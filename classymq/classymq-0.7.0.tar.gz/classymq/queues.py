from twisted.internet.defer import inlineCallbacks, returnValue
from uuid import uuid4
import logging
from classymq import common
__author__ = 'gdoermann'

logger = logging.getLogger(__name__)

class BaseQueue(object):
    KEY=''
    TICKET=0
    PASSIVE=False
    DURABLE=False
    EXCLUSIVE=False
    AUTO_DELETE=False
    NOWAIT=False

    def __init__(self, **params):
        super(BaseQueue, self).__init__()
        self.params = params
        self.uuid = str(uuid4())
        self.params['instance_uuid'] = self.uuid

    def key(self, params=None):
        full_params = {}
        full_params.update(self.params)
        if params:
            full_params.update(params)
        return self.KEY.format(**full_params)

    def kwargs(self, arguments=None, key_params=None, **extras):
        if arguments is None: arguments = {}
        if key_params is None: key_params = {}
        key_params.update(self.params)
        key = self.key(key_params)
        logger.debug('Connecting to queue: {}'.format(key))
        kwargs = {
            'ticket': self.TICKET,
            'queue': key,
            'passive':self.PASSIVE,
            'durable':self.DURABLE,
            'exclusive':self.EXCLUSIVE,
            'auto_delete':self.AUTO_DELETE,
            'nowait':self.NOWAIT,
            'arguments':arguments
        }
        kwargs.update(extras)
        return kwargs

    def pika_declare(self, channel, callback=None, arguments=None, key_params=None):
        """
        This will create a pika queue that can be used for non-twisted services
        """
        return channel.queue_declare(**self.kwargs(callback=callback, arguments=arguments, key_params=key_params))

    @inlineCallbacks
    def txamqp_declare(self, channel, arguments=None, key_params=None, **kwargs):
        """
        This creates a txamqp queue in a twisted way.
        """
        kwargs = self.kwargs(arguments=arguments, key_params=key_params, **kwargs)
        queue = yield channel.queue_declare(**kwargs)
        returnValue(queue)

class BaseTemporaryQueue(BaseQueue):
    AUTO_DELETE = True


class BasePrefixRoutingQueue(BaseQueue):
    PREFIX = lambda *args: common.resolve_setting('LOCAL_ROUTING_PREFIX', '')

    def key(self, params=None):
        if params is None:
            params = {}
        prefix = self.PREFIX()
        return '{}{}'.format(prefix, super(BasePrefixRoutingQueue, self).key(params))

