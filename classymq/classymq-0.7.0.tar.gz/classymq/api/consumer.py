from classymq.api import common
from classymq.lib.uuid import UUIDConsumer
import logging

log = logging.getLogger(__name__)

class AMQPAPIConsumer(UUIDConsumer):
    EXCHANGE = common.AMQPAPIExchange
    QUEUE = common.AMQPAPIQueue
    MESSAGE_CLASS = common.AMQPAPIRequest

    def __init__(self, uuid, prefix, key_params=None, rate=None, routing_keys=None):
        if key_params is None: key_params = {}
        key_params['prefix'] = prefix
        super(AMQPAPIConsumer, self).__init__(uuid, key_params, rate, routing_keys)

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.uuid)
