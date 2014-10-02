from twisted.internet.defer import inlineCallbacks, returnValue
from classymq.factory import AmqpFactory

__author__ = 'gdoermann'

class ConsumerService(object):
    consumer_klass = None
    consumer = None

    def __init__(self):
        super(ConsumerService, self).__init__()

    def create_consumer(self):
        if not self.consumer:
            self.consumer = self.consumer_klass()
        return self.consumer

    @inlineCallbacks
    def connect_to_amqp(self):
        """
        Opens the connection to FreeSWITCH.
        """
        self.amqp_factory = AmqpFactory(log_level=5)
        connection = yield self.amqp_factory.connect()
        self.create_consumer()
        self.amqp_factory.read(self.consumer)
        returnValue(connection)

    def run(self):
        self.connect_to_amqp()
