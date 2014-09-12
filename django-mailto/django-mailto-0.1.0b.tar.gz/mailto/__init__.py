# -*- coding: utf-8 -*-
import logging

from mailto.utils import get_celery_worker_status
from models import mailto as _mailto

try:
    from tasks import task_mailto
except ImportError:
    pass

log = logging.getLogger(__name__)


def mailto(*args, **kwargs):
    """
from mail import mailto
mailto('foo', ['m@handerek.net', ])
    """
    try:
        celery_status = get_celery_worker_status()
        if not celery_status:
            raise Exception
        task_mailto.apply_async((args, kwargs))
    except Exception as e:
        log.warn(e)
        _mailto(*args, **kwargs)