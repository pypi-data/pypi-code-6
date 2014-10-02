import json
from classymq import common, exchanges
from classymq.common import pika_connection
import pika

__author__ = 'gdoermann'


class AMQPProducer(object):
    ROUTING_KEY=None
    EXCHANGE=None
    DELIVERY_MODE=common.NON_PERSISTENT
    CONSUMER=None
    VHOST = None

    def __init__(self, consumer_klass=None, key_params=None):
        if key_params is None: key_params = {}
        self.key_params = key_params
        super(AMQPProducer, self).__init__()
        consumer_klass = consumer_klass or self.CONSUMER
        self.consumer = consumer_klass

        exchange_klass =  self.EXCHANGE or self.consumer and self.consumer.EXCHANGE or exchanges.BaseTemporaryExchange
        self.exchange = exchange_klass(**key_params)

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
    def amqp_connection(self):
        if not getattr(self, '_amqp_connection', None):
            self._amqp_connection = pika_connection()
        return self._amqp_connection

    @property
    def amqp_channel(self):
        return self.amqp_connection.channel()

    def message_routing_key(self, msg, *args, **kwargs):
        if getattr(msg, 'routing_key', None):
            return msg.routing_key(*args, **kwargs)
        key = self.routing_key
        return key.format(**self.key_params)

    def push(self, obj, *args, **kwargs):
        raw = self.clean(obj)
        val = self.push_text(raw=raw, *args, **kwargs)
        return val

    def _routing_key(self, *args, **kwargs):
        """
        Allow for routing_key to be changed in the moment
        """
        return kwargs.get('routing_key', None) is not None and \
               kwargs.get('routing_key') or self.routing_key

    def clean(self, raw):
        return raw

    def push_text(self, *args, **kwargs):
        raw = kwargs.pop('raw', None)
        self.send_message(raw, *args, **kwargs)
        return None

    def send_message(self, message, close=True):
        #TODO: Make this add to amqp queue directly...
        self.amqp_channel.basic_publish(exchange=self.exchange_name,
            routing_key=self.message_routing_key(message),
            body=str(message),
            properties=pika.BasicProperties(
                delivery_mode = self.DELIVERY_MODE,
            ))
        if close:
            self.amqp_close()

    def amqp_close(self):
        self.amqp_connection.close()
        self._amqp_connection = None


class JsonProducer(AMQPProducer):
    """
    Allows for pushing of json objects
    JsonConsumers will need to unserialize the objects on the other end.
    """
    def clean(self, raw):
        data = json.dumps(raw)
        return data

    def message_routing_key(self, msg, *args, **kwargs):
        key = self._routing_key(*args, **kwargs)
        params = {}
        params.update(self.key_params)
        if isinstance(msg, dict):
            params.update(msg)
        return key.format(**params)
