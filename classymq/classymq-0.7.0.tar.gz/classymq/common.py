import os
from twisted.internet.error import ConnectionRefusedError
from twisted.internet.defer import inlineCallbacks, returnValue
import pika

try:
    # Handle django settings if they use django.
    from django.conf import settings
except ImportError:
    # If django not used, fall back to environment variables
    settings = None

def resolve_setting(name, default):
    if settings:
        return getattr(settings, name, default)
    else:
        return os.environ.get(name, default)

__author__ = 'gdoermann'

NON_PERSISTENT = 1
PERSISTENT = 2

dirname = os.path.dirname(__file__)

RABBIT_MQ_HOST = resolve_setting('RABBIT_MQ_HOST', 'localhost')
RABBIT_MQ_PORT = resolve_setting('RABBIT_MQ_PORT', 5672)

AMQP_SPEC = resolve_setting('AMQP_SPEC', os.path.join(dirname, 'spec.xml'))
VHOST = resolve_setting('VHOST', '/')
EXCHANGE_NAME = resolve_setting('EXCHANGE_NAME', 'classyexchange')
QUEUE_NAME = resolve_setting('QUEUE_NAME', 'classyqueue')
ROUTING_KEY = resolve_setting('ROUTING_KEY', '')
CONSUMER_TAG = resolve_setting('CONSUMER_TAG', 'classyconsumer')

credentials = resolve_setting('RABBIT_CREDENTIALS', {'USERNAME':'guest', "PASSWORD":"guest"})

@inlineCallbacks
def getConnection(client):
    conn = yield client.connectTCP(RABBIT_MQ_HOST, RABBIT_MQ_PORT)
    # start the connection negotiation process, sending security mechanisms
    # which the client can use for authentication
    try:
        yield conn.start(credentials)
    except Exception:
        raise ConnectionRefusedError()
    returnValue(conn)


@inlineCallbacks
def getChannel(conn, channel_id=3):
    # create a new channel that we'll use for sending messages; we can use any
    # numeric id here, only one channel will be created; we'll use this channel
    # for all the messages that we send
    chan = yield conn.channel(channel_id)
    # open a virtual connection; channels are used so that heavy-weight TCP/IP
    # connections can be used my multiple light-weight connections (channels)
    yield chan.channel_open()
    returnValue(chan)


def pika_connection(channel_max=0, heartbeat=False, **kwargs):
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT,
        virtual_host=VHOST, channel_max=channel_max, heartbeat=heartbeat,
        credentials=pika.credentials.PlainCredentials(credentials['LOGIN'], credentials['PASSWORD']),
        **kwargs
    ))