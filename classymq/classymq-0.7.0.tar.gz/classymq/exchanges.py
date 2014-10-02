from twisted.internet.defer import inlineCallbacks, returnValue
from uuid import uuid4
from classymq import common
import logging

logger = logging.getLogger(__name__)

__author__ = 'gdoermann'

class EXCHANGE_TYPES:
    DIRECT='direct'
    TOPIC='topic'
    HEADERS='headers'
    FANOUT='fanout'

class BaseExchange(object):
    KEY=common.EXCHANGE_NAME
    TICKET=0
    TYPE=EXCHANGE_TYPES.DIRECT
    PASSIVE=False
    DURABLE=False
    AUTO_DELETE=False
    INTERNAL=False
    NOWAIT=False

    def key(self, params=None, **extra_params):
        full_params = {}
        full_params.update(self.params)
        if params:
            full_params.update(params)
        full_params.update(extra_params)
        return self.KEY.format(**full_params)

    def __init__(self, **params):
        self.uuid = str(uuid4())
        super(BaseExchange, self).__init__()
        self.params = params
        self.params['instance_uuid'] = self.uuid

    def kwargs(self, arguments=None, key_params=None, **extras):
        if arguments is None: arguments = {}
        if key_params is None: key_params = {}
        key = self.key(key_params)
        logger.debug('Connecting to exchange: {}'.format(key))
        kwargs = {
            'ticket': self.TICKET,
            'exchange':key,
            'type':self.TYPE,
            'passive':self.PASSIVE,
            'durable':self.DURABLE,
            'auto_delete':self.AUTO_DELETE,
            'internal':self.INTERNAL,
            'nowait':self.NOWAIT,
            'arguments': arguments
            }
        kwargs.update(extras)
        return kwargs

    def pika_declare(self, channel, callback=None, arguments=None, key_params=None):
        """
        This will create a pika exchange that can be used for non-twisted services
        """
        return channel.exchange_declare(**self.kwargs(callback=callback, arguments=arguments, key_params=key_params))

    @inlineCallbacks
    def txamqp_declare(self, channel, arguments=None, key_params=None):
        """
        This creates a txamqp exchange in a twisted way.
        """
        kwargs = self.kwargs(arguments=arguments, key_params=key_params)
        exch = yield channel.exchange_declare(**kwargs)
        returnValue(exch)

class BaseTemporaryExchange(BaseExchange):
    AUTO_DELETE = True
    DURABLE = False


class BasePrefixRoutingExchange(BaseExchange):
    PREFIX = lambda *args: common.resolve_setting('LOCAL_ROUTING_PREFIX', '')

    def key(self, params=None):
        if params is None:
            params = {}
        prefix = self.PREFIX()
        return '{}{}'.format(prefix, super(BasePrefixRoutingExchange, self).key(params))

