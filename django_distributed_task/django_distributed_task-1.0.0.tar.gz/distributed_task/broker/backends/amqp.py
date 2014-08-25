from __future__ import unicode_literals

# TODO move to local settings
from distributed_task import settings
import pika
from ..interface import BrokerInterface
from distributed_task.core.serializer import serialize, deserialize
from distributed_task.exceptions import BrokerConnectionError, ConnectionClosed
from pika.exceptions import AMQPConnectionError, ConnectionClosed as PikaConnectionClosed


class AMQPMessageBroker(BrokerInterface):

    connection = None
    channel = None
    host = None
    user = None
    secret = None
    port = None
    queue = None
    conn_retry = 0

    def prepare(self):
        self.load_config()
        self.connect()

    def load_config(self):
        OPTIONS = getattr(settings, 'BROKER_OPTIONS')

        self.host = OPTIONS.get('HOST', 'localhost')
        self.user = OPTIONS.get('USERNAME', 'guest')
        self.secret = OPTIONS.get('PASSWORD', 'guest')
        self.port = OPTIONS.get('PORT', 5672)
        self.queue = OPTIONS.get('QUEUE', 'distributed_task_queue')

    def connect(self):
        if self.connection:
            return

        params = pika.ConnectionParameters(host=self.host, port=self.port)

        try:
            self.connection = pika.BlockingConnection(params)
        except AMQPConnectionError, e:
            raise BrokerConnectionError(e)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def produce_message(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=serialize(data))

    def consume_message(self, handler):
        def callback(ch, method, properties, body):
            handler(deserialize(body))

        try:
            self.channel.basic_consume(callback, queue=self.queue, no_ack=True)
        except PikaConnectionClosed, e:
            raise ConnectionClosed(e)

    def keep_consuming(self, handler):

        try:
            self.consume_message(handler)
            self.channel.start_consuming()
        except (PikaConnectionClosed, ConnectionClosed):
            self.connect()
            self.keep_consuming(handler)
