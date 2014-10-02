import sys
from classymq import consumers
from classymq.event import common, events
from classymq.event.registry import registry
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor
import logging

log = logging.getLogger(__name__)


class EventConsumer(consumers.JsonMessageConsumer):
    """
    This is a topic consumer, so you will usually specify one or more routing keys
    following the producer topic key template: <subject>.<event>.<uuid>

    Topic consumers also automatically bind to their own uuid.

    The processor will pass in Event classes.
    """
    EXCHANGE = common.EventExchange
    QUEUE = common.EventQueue
    ROUTING_KEY = "#" # Subscribe to all to begin with
    MESSAGE_CLASS = events.BaseEvent

class ModelEventConsumer(EventConsumer):
    ROUTING_KEY = "{action}.{models}.#"
    MESSAGE_CLASS = events.ModelEvent
    ACTION = '*'

    def __init__(self, models='*', key_params=None, rate=None, routing_keys=None):
        if key_params is None: key_params = {}
        key_params['models'] = models
        key_params['action'] = self.ACTION
        super(ModelEventConsumer, self).__init__(key_params, rate, routing_keys)

class CreationEventConsumer(ModelEventConsumer):
    MESSAGE_CLASS = events.CreationEvent
    ACTION = 'creation'

class ActivationEventConsumer(ModelEventConsumer):
    MESSAGE_CLASS = events.ActivationEvent
    ACTION = 'activation'

class UpdateEventConsumer(ModelEventConsumer):
    MESSAGE_CLASS = events.UpdateEvent
    ACTION = 'update'

@inlineCallbacks
def main():
    from classymq.factory import AmqpFactory
    factory = AmqpFactory()
    yield factory.connect()

    def printme(msg):
        log.info(msg)
    consumer = ModelEventConsumer()
    consumer.processor.register(printme)
    factory.read(consumer)
    returnValue(None)

if __name__ == "__main__":
    if not sys.argv != 2:
        print "{} content".format(sys.argv[0])
        exit(1)
    main()
    reactor.run()

