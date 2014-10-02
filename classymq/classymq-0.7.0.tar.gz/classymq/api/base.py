import logging
from twisted.internet import defer
from twisted.internet.defer import inlineCallbacks, returnValue
from uuid import uuid4
from classymq.api.common import AMQPAPIRequest
from classymq.api.producer import AMQPAPIProducer, SyncAMQPAPIProducer
from classymq.api.consumer import AMQPAPIConsumer

__author__ = 'gdoermann'

logger = logging.getLogger(__name__)

class AMQPAPI(object):
    PRODUCER_CLASS = AMQPAPIProducer
    SYNC_PRODUCER_CLASS = SyncAMQPAPIProducer
    CONSUMER_CLASS = AMQPAPIConsumer
    MESSAGE_CLASS = AMQPAPIRequest
    PREFIX = 'amqpapi'

    def __init__(self, amqp_factory, handler=None, uuid=None, prefix=None):
        """
        @type amqp_factory: AmqpFactory, AmapFactories
        """
        self.deferred_until_connected = defer.Deferred()
        self.prefix = prefix or self.PREFIX
        super(AMQPAPI, self).__init__()
        self.uuid = uuid or self._generate_uuid()
        self.amqp_factory = amqp_factory
        self.jobs = {}
        self.handler = handler
        self.initialize()

    @inlineCallbacks
    def initialize(self):
        logger.debug('Creating api consumer')
        yield self.create_consumer()
        yield self.consumer.processor.register(self.handle_response)
        logger.debug('Reading from consumer')
        yield self.amqp_factory.read(self.consumer)
        yield self.consumer.defer_until_reading

        logger.debug('Creating Producer')
        yield self.create_producer()
        if not self.deferred_until_connected.called:
            self.deferred_until_connected.callback(None)
        logger.debug('Setup finished')

    def create_producer(self):
        self.producer = self.PRODUCER_CLASS(self.amqp_factory)

    def create_consumer(self):
        self.consumer = self.CONSUMER_CLASS(self.uuid, prefix=self.prefix)

    def _generate_uuid(self):
        return str(uuid4())

    @classmethod
    def serialize(cls, msg):
        return msg

    def unserialize(self, msg):
        return msg

    def send_to(self, uuid, message, correlation_id=None, **kwargs):
        msg = self.serialize(message)
        request = self.MESSAGE_CLASS(uuid=self.uuid, message=msg, correlation_id=correlation_id,
            reply_to=correlation_id and self.uuid or None)
        request.update(kwargs)
        logger.debug('Pushing request: %s to %s' % (request, uuid))
        self.producer.push(request, uuid=uuid)

    def __call__(self, consumer_uuid, command, **kwargs):
        job_uuid = self._generate_uuid()
        d = defer.Deferred()
        # send it over the line!
        self.jobs[job_uuid] = d
        self.send_to(consumer_uuid, command, correlation_id=job_uuid)
        return d

    @inlineCallbacks
    def handle_response(self, response):
        msg = response.message
        logger.debug('Received Response: %s' % response)
        message = self.unserialize(msg)
        reply_to = response.get('reply_to', None)
        correlation_id = response.get('correlation_id', None)
        if correlation_id and self.jobs.has_key(correlation_id):
            d = self.jobs.pop(correlation_id)
            d.callback(message)
            returnValue(None)
        if self.handler:
            message = yield self.handler(response.message, server=reply_to)
            self.send_to(reply_to, message, correlation_id)
        yield

    @inlineCallbacks
    def close(self):
        yield self.consumer.close()
        yield self.amqp_factory.stop_consuming(self.consumer)

    @classmethod
    def synchronous_send(cls, uuid, message, **kwargs):
        msg = cls.serialize(message)
        request = cls.MESSAGE_CLASS(uuid=uuid, message=msg, reply_to=None)
        request.update(kwargs)
        logger.debug('Pushing request: %s to %s' % (request, uuid))
        producer = cls.SYNC_PRODUCER_CLASS()
        producer.push(request, uuid=uuid)
