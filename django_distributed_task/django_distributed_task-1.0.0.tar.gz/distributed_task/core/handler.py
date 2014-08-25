from __future__ import unicode_literals
from distributed_task.utils.module_loading import import_string
from time import time
import logging
logger = logging.getLogger(__name__)


def task_handler(obj):
    try:
        command = obj.get('cmd')
    except KeyError:
        logger.exception("Missing 'cmd' key in message: '%r'. Operation aborted.", obj)
        return

    args = obj.get('args', [])
    kwargs = obj.get('kwargs', {})

    fnc = import_string(command)

    start_time = time()
    r = None

    try:
        r = fnc(*args, **kwargs)
    except (Exception, BaseException), e:
        # Here's a good point to mail the exception
        # TODO Send Exception Mail
        pass
    except:
        # We keep it running
        pass

    duration = time() - start_time

    logger.info("executed task=%s args=%r kwargs=%r time=%f response=%r", command, args, kwargs, duration, r)