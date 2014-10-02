import logging
from classymq import exchanges, queues
from classymq.lib.uuid import UUIDRequest

log = logging.getLogger(__name__)

class AMQPAPIRequest(UUIDRequest):
    def __init__(self, uuid=None, message=None, *args, **kwargs):
        super(AMQPAPIRequest, self).__init__(uuid, *args, **kwargs)
        self.message = message

    def __str__(self):
        d = {}
        for k, v in self.items():
            sv = str(v)
            if len(sv) > 500:
                sv = sv[:500] + '...'
            d[k] = sv
        return str(d)


class AMQPAPIExchange(exchanges.BaseExchange):
    KEY = "amqpapi"
#    TYPE = exchanges.EXCHANGE_TYPES.TOPIC

class AMQPAPIQueue(queues.BaseQueue):
    KEY = "amqpapi-%(prefix)s-%(uuid)s"
    AUTO_DELETE = True
