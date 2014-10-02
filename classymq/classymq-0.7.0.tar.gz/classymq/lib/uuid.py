from classymq import consumers, producers
from classymq import synchronous
from classymq.message import AmqpMessage

__author__ = 'gdoermann'

class UUIDRequest(AmqpMessage):
    """
    A request that passes a FS event across the intranets
    """
    def __init__(self, uuid=None, *args, **kwargs):
        super(UUIDRequest, self).__init__(*args, **kwargs)
        self.uuid = uuid

class UUIDConsumer(consumers.JsonMessageConsumer):
    ROUTING_KEY = "%(uuid)s"
    MESSAGE_CLASS = UUIDRequest

    def __init__(self, uuid, key_params=None, rate=None, routing_keys=None):
        self.uuid = uuid
        if key_params is None: key_params = {}
        key_params.update({'uuid': self.uuid})
        super(UUIDConsumer, self).__init__(key_params, rate, routing_keys)

class UUIDProducer(producers.JsonProducer):
    ROUTING_KEY = "%(uuid)s"
    CONSUMER = UUIDConsumer

class SyncUUIDProducer(synchronous.JsonProducer):
    ROUTING_KEY = "%(uuid)s"
    CONSUMER = UUIDConsumer