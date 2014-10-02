import sys
from classymq import producers
from classymq.event import consumer, events
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor

class EventProducer(producers.JsonProducer):
    """
    This is a topic event producer.  When a message is sent it will
    be delivered to everyone who is listening.
    """
    CONSUMER = consumer.EventConsumer
    ROUTING_KEY="{subject}.{event}.{uuid}"

class CreationEventProducer(EventProducer):
    CONSUMER = consumer.CreationEventConsumer
    ROUTING_KEY='creation.{model}.{pk}'

    def message_routing_key(self, msg, *args, **kwargs):
        return super(CreationEventProducer, self).message_routing_key(msg, *args, **kwargs)

class ActivationEventProducer(EventProducer):
    CONSUMER = consumer.ActivationEventConsumer
    ROUTING_KEY='activation.{model}.{pk}'

    def message_routing_key(self, msg, *args, **kwargs):
        return super(ActivationEventProducer, self).message_routing_key(msg, *args, **kwargs)

class UpdateEventProducer(EventProducer):
    CONSUMER = consumer.UpdateEventConsumer
    ROUTING_KEY='update.{model}.{pk}'

    def message_routing_key(self, msg, *args, **kwargs):
        return super(UpdateEventProducer, self).message_routing_key(msg, *args, **kwargs)

@inlineCallbacks
def main():
#    producer = CreationEventProducer()
    dproducer = ActivationEventProducer()
#    yield producer.push(events.CreationEvent('Campaign', 1))
    yield dproducer.push(events.ActivationEvent('Campaign', 2, active=True))
#    yield producer.close()
    yield dproducer.close()
    yield reactor.stop()

if __name__ == "__main__":
    if not sys.argv != 2:
        print "{} content".format(sys.argv[0])
        exit(1)
    main()
    reactor.run()
