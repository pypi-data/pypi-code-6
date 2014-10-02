import logging
from logging.handlers import RotatingFileHandler
import platform
from twisted.internet.defer import inlineCallbacks, returnValue

from txamqp.client import Closed


__author__ = 'gdoermann'

HOSTNAME = platform.node()

class TwistedAMQPHandler(logging.Handler):
    """Provides a handler for passing Python logging messages into an AMQP
      message queuing system."""
    def __init__(self,  producer_klass=None, level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)
        self.producer = None
        self.producer_klass = producer_klass
        self.amqp_factory = None

    @inlineCallbacks
    def connect_to_amqp(self):
        """
        Opens the connection to FreeSWITCH.
        """
        from classymq.factory import AmqpFactory
        self.amqp_factory = AmqpFactory()
        connection = yield self.amqp_factory.connect()
        returnValue(connection)

    @inlineCallbacks
    def emit(self, record):
        if not self.producer:
            if not self.amqp_factory:
                yield self.connect_to_amqp()
            if self.producer_klass is None:
                from classymq.log import producer
                self.producer_klass = producer.LogProducer
            self.producer = self.producer_klass(self.amqp_factory)
        message = yield self.format(record)
        routing_key = "{}.{}.{}" .format(HOSTNAME, record.name, record.levelname)
        message_dict = dict(( (k,v) for k, v in record.__dict__.items() if isinstance(
                    v, (basestring, int, float,) ) ))
        msg = {
            'extras': message_dict,
            'message': message,
            'hostname': HOSTNAME
        }
        try:
            yield self.producer.push(msg, routing_key=routing_key)
        except Closed:
            # This log message will be lost
            pass
        returnValue(None)


class AmqpRotatingHandler(RotatingFileHandler):
    pass

class AmqpLogger(logging.Logger):
    """
    This logger allows you to override anything you want in the logger dict.
    This allows you to log messages from other machines and show the log
    messages as they would appear on that machine, not from the emitter
    on the amqp handler.
    """

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is None: extra = {'hostname': None}
        for key in extra:
            rv.__dict__[key] = extra[key]
        return rv
