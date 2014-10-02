from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from txamqp.client import TwistedDelegate
import txamqp
from classymq import common
from classymq.protocol import AmqpProtocol, ManualMessage, ProducerMessage

__author__ = 'gdoermann'

class AmqpFactory(protocol.ReconnectingClientFactory):
    protocol = AmqpProtocol

    def __init__(self, spec_file=None, vhost=None, host=None, port=None, credentials=None, log_level=None):
        spec_file = spec_file or common.AMQP_SPEC
        self.spec = txamqp.spec.load(spec_file)
        self.credentials = credentials or common.credentials
        self.vhost = vhost or common.VHOST
        self.host = host or common.RABBIT_MQ_HOST
        self.port = port or common.RABBIT_MQ_PORT
        self.delegate = TwistedDelegate()
        self.deferred = Deferred()

        self.instance = None # The protocol instance.

        self.message_queue = [] # List of messages waiting to be sent.
        self.consumers = [] # List of message consumers to listen on.

    @inlineCallbacks
    def connect(self):
        # Make the TCP connection.
        connection = yield reactor.connectTCP(self.host, self.port, self)
        returnValue(connection)

    def buildProtocol(self, addr):
        instance = self.protocol(self.delegate, self.vhost, self.spec)

        instance.factory = self
        self.instance = instance
        self.client = instance

        self.resetDelay()
        for consumer in self.consumers:
            self.read(consumer)
        return instance


    def clientConnectionFailed(self, connector, reason):
        print("Connection Failed.")
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


    def clientConnectionLost(self, connector, reason):
        print("Client connection lost.")
        self.instance = None

        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def manual_send(self, exchange=None, routing_key=None, msg=None):
        msg = (exchange, routing_key, msg)
        self.message_queue.append(ManualMessage(exchange, routing_key, msg))

    @inlineCallbacks
    def send_message(self, message, producer, **extras):
        """Send a message."""
        # Add the new message to the queue.
        self.message_queue.append(ProducerMessage(producer, message, extras))

        # Send all queued messages.
        if self.instance is not None:
            yield self.instance.send()

    def read(self, consumer):
        """
        Configure an exchange to be read from.
        This should be a Consumer instance
        """
        # Add this to the read list so that we have it to re-add if we lose the connection.
        if consumer not in self.consumers:
            self.consumers.append(consumer)

        # Tell the protocol to read this if it is already connected.
        if self.instance is not None:
            self.instance.read(consumer)
            consumer.protocol = self.instance
