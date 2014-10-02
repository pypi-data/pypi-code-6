import collections
import logging
import traceback
from twisted.internet import defer
from twisted.internet.defer import inlineCallbacks, returnValue

from txamqp.protocol import AMQClient
from txamqp.content import Content

__author__ = 'gdoermann'

logger = logging.getLogger(__name__)

ManualMessage = collections.namedtuple('ManualMessage', ('exchange', 'routing_key', 'msg'))
ProducerMessage = collections.namedtuple('ProducerMessage', ('producer', 'message', 'extras'))

class AmqpProtocol(AMQClient):
    """The protocol is created and destroyed each time a connection is created and lost."""
    _channel = 1
    factory = None

    def __init__(self, *args, **kwargs):
        self.lock = defer.DeferredLock()
        AMQClient.__init__(self, *args, **kwargs)

    def get_channel_number(self):
        """
        This allows you to change the channel and add logic to how you choose channels.
        """
        return self._channel

    @inlineCallbacks
    def connectionMade(self):
        """Called when a connection has been made."""
        AMQClient.connectionMade(self)
        self.default_log_level = self.factory.log_level is not None and self.factory.log_level or self.default_log_level

        # Flag that this protocol is not connected yet.
        self.connected = False

        # Authenticate.
        try:
            yield self.start(self.factory.credentials)
        except Exception:
            logger.error("Authentication failed: {}".format(traceback.format_exc()))
            returnValue(None)

        # Authenticated!
        try:
            self.chan = yield self.channel(self.get_channel_number())
        except Exception:
            logger.error("Failed to get channel: {}".format(traceback.format_exc()))
            returnValue(None)

        # You now have a channel!
        try:
            yield self.chan.channel_open()
        except Exception:
            logger.error("Failed to open channel: {}".format(traceback.format_exc()))
            returnValue(None)

        # Mark the connection as open.
        self.connected = True
        logger.info('AMQP connection made.')

        # Now that the channel is open add any readers the user has specified.
        for consumer in self.factory.consumers:
            self.read(consumer)

        # Send any messages waiting to be sent.
        self.send()

        # Fire the factory's 'initial connect' deferred if it hasn't already
        if not self.factory.deferred.called:
            self.factory.deferred.callback(self)

    @inlineCallbacks
    def read(self, consumer):
        """Add an exchange to the list of exchanges to read from."""
        queue = None
        if self.connected:
            # Connection is already up. Add the reader.
            try:
                queue = yield self.setup_read(consumer)
            except Exception:
                logger.error(traceback.format_exc())
                returnValue(None)
        else:
            # Connection is not up. _channel_open will add the reader when the
            # connection is up.
            logger.warning("No AMQP connection.")
            returnValue(None)

        while self.connected:
            msg = None
            try:
                msg = yield queue.get()
            except Exception:
                logger.error('Error reading from queue: %s' % traceback.format_exc())
                self.setup_read(consumer)
                returnValue(None)
            try:
                self.process_message(consumer, msg)
                yield consumer.rate_limit()
            except Exception:
                logger.error('Error processing message %s: %s' % (msg, traceback.format_exc()))

    # Send all messages that are queued in the factory.
    @inlineCallbacks
    def send(self):
        """If connected, send all waiting messages."""
        if self.lock.locked:
            returnValue(None)
        yield self.lock.acquire()
        try:
            if self.connected:
                while len(self.factory.message_queue) > 0:
                    message = self.factory.message_queue.pop(0)
                    yield self._send_message(message)
        finally:
            self.lock.release()

    # Do all the work that configures a listener.
    @inlineCallbacks
    def setup_read(self, consumer):
        """This function does the work to read from an exchange.
        @type consumer: consumers.MessageConsumer
        """
        yield consumer.exchange_instance.txamqp_declare(self.chan, key_params=consumer.key_params)
        yield consumer.queue_instance.txamqp_declare(self.chan, key_params=consumer.key_params)

        # Declare the queue and bind to it.
        for key in consumer.routing_keys:
            yield self.chan.queue_bind(queue=consumer.queue_key, exchange=consumer.exchange_key, routing_key=key)

        yield self.chan.basic_consume( queue=consumer.queue_key, consumer_tag=consumer.consumer_tag)
        queue = yield self.queue(consumer.consumer_tag)
        returnValue(queue)

    @inlineCallbacks
    def process_message(self, consumer, message):
        """This function processes a single message
            @type consumer: MessageConsumer
        """
        if message:
            message = yield consumer.clean(message)
            try:
                yield consumer.processor.txnotify(message.content.body)
            except Exception:
                logger.error(traceback.format_exc())
            yield self.chan.basic_ack(message.delivery_tag)
            self.log('Sent acknowledgement to AMQP server')
            returnValue(None)
        else:
            logger.warning('No message received')

    @inlineCallbacks
    def _send_message(self, message):
        """Send a single message."""
        # First declare the exchange just in case it doesn't exist.
        if isinstance(message, ManualMessage):
            # Manual messages are NON DURABLE and exchanges are automatically deleted!
            yield self.chan.exchange_declare(exchange=message.exchange, type="direct", durable=False, auto_delete=True)
            msg = Content(message.msg)
            try:
                yield self.chan.basic_publish(exchange=message.exchange, routing_key=message.routing_key, content=msg)
            except Exception:
                logger.error("Sending message failed: %s" % traceback.format_exc())
        elif isinstance(message, ProducerMessage):
            producer = message.producer
            msg = Content(producer.clean(message.message))
            msg["delivery mode"] = producer.message_persistance
            extras = message.extras or {}
            yield self.chan.basic_publish(
                exchange=producer.exchange_name, content=msg,
                routing_key=producer.message_routing_key(message.message, **extras))
        else:
            logger.error("Unknown message type: {}".format(type(message)))

    def close(self, reason):
        yield self.chan.channel_close()
        AMQClient.close(self, reason)
