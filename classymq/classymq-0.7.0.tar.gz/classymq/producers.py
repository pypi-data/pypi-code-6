import json
import logging
from twisted.internet.defer import inlineCallbacks, returnValue
import txamqp.spec
from classymq import common, exchanges

__author__ = 'gdoermann'

logger = logging.getLogger(__name__)

SPEC = txamqp.spec.load(common.AMQP_SPEC)

class MessageProducer(object):
    """
    This is the base message producer class.
    A message producer will create amqp messages.  It knows how to
    set itself up (create connections to amqp and get channels)
    as well as how to publish to the exchanges.

    Setup is done resolving variables in the following order:
        1. Variables set on the class: ROUTING_KEY, EXCHANGE, SPEC, and VHOST that are
            set on the class itself will be used
        2. If the class is initialized with a consumer_klass it will take all of it's
            properties off of the consumer class
        3. If the class as a CONSUMER declared, this is the default consumer_klass

    This allows for dynamic creation, inheritance and all other advantages of classes
    for exchanges, routing and hosts.
    """
    ROUTING_KEY=None
    EXCHANGE=None
    SPEC=None
    VHOST=None
    MESSAGE_PERSISTENCE = common.NON_PERSISTENT
    CONSUMER = None

    factory = None

    def __init__(self, factory, consumer_klass=None, key_params=None):
        super(MessageProducer, self).__init__()
        self.chan = self.conn = None
        self.consumer = consumer_klass or self.CONSUMER
        if key_params is None: key_params = {}
        self.key_params = key_params
        self.delegate = None
        self.factory = factory

        exchange_klass =  self.EXCHANGE or self.consumer and self.consumer.EXCHANGE or exchanges.BaseTemporaryExchange
        self.exchange = exchange_klass(**key_params)

    @property
    def message_persistance(self):
        """
        Persistence should not be decided by the consumer, but by the producer.
        """
        return self.MESSAGE_PERSISTENCE

    @property
    def vhost(self):
        value = self.VHOST or self.consumer and self.consumer.VHOST or common.VHOST
        return value.format(**self.key_params)

    @property
    def routing_key(self):
        value = self.ROUTING_KEY or self.consumer and self.consumer.ROUTING_KEY or common.ROUTING_KEY
        return value

    @property
    def exchange_name(self):
        return self.exchange.key()

    @property
    def spec(self):
        return self.SPEC or self.consumer and self.consumer.SPEC

    def _routing_key(self, *args, **kwargs):
        """
        Allow for routing_key to be changed in the moment
        """
        return kwargs.get('routing_key', None) is not None and \
               kwargs.get('routing_key') or self.routing_key

    @inlineCallbacks
    def push(self, obj, *args, **kwargs):
        val = yield self.push_text(raw=obj, *args, **kwargs)
        returnValue(val)

    def message_routing_key(self, msg, *args, **kwargs):
        key = self._routing_key(*args, **kwargs)
        return key.format(**self.key_params)

    def clean(self, raw):
        return raw

    @inlineCallbacks
    def push_text(self, *args, **kwargs):
        raw = kwargs.pop('raw', None)
        logger.debug('Sending message: {}'.format(raw))
        yield self.factory.send_message(raw, self, **kwargs)
        returnValue(None)

class JsonProducer(MessageProducer):
    """
    Allows for pushing of json objects
    JsonConsumers will need to unserialize the objects on the other end.
    """
    def clean(self, raw):
        data = json.dumps(raw)
        return data

    @inlineCallbacks
    def direct_push(self, uuid, obj, *args, **kwargs):
        val = yield self.push(obj, routing_key=uuid, *args, **kwargs)
        returnValue(val)

    def message_routing_key(self, msg, *args, **kwargs):
        key = self._routing_key(*args, **kwargs)
        params = {}
        params.update(self.key_params)
        if isinstance(msg, dict):
            params.update(msg)
        return key.format(**params)
