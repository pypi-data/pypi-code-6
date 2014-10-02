from optparse import OptionParser
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor, defer
import logging

from classymq import consumers
from examples.log import common

log = logging.getLogger(__name__)

class LogConsumer(consumers.JsonMessageConsumer):
    EXCHANGE = common.LogExchange
    QUEUE = common.LogQueue
    ROUTING_KEY = '#'
    MESSAGE_CLASS = common.LogMessage

    def __init__(self, key_params=None, rate=None, routing_keys=None):
        super(LogConsumer, self).__init__(key_params, rate, routing_keys)
        self.processor.register(self.emit)

    def emit(self, message):
        level = 10
        if message.extras:
#            print message.extras.keys()
            level = logging.getLevelName(message.extras['levelname'])
            msg = message.extras['msg']
        else:
            message.extras = { }
            msg = message.message

        if message.has_key('hostname') and message.hostname:
            message.extras['hostname'] = message.hostname
        else:
            message.extras['hostname'] = None
        log.log(level, msg, extra=message.extras)

@inlineCallbacks
def main(args, opts):
    from classymq.factory import AmqpFactory
    consumer = LogConsumer(key_params=opts)

    factories = []
    if args:
        dlist = []
        for host in args:
            factory = AmqpFactory(host=host, credentials=common.RABBIT_CREDENTIALS)
            d = factory.connect()
            dlist.append(d)
            factories.append(factory)
            factory.read(consumer)
        yield defer.DeferredList(dlist)
    else:
        factory = AmqpFactory()
        yield factory.connect()
        factories.append(factory)
        factory.read(consumer)

    returnValue(None)

if __name__ == "__main__":
    parser = OptionParser(description="Pass in amqp queue keys to listen to.  Default is # for all messages.")
    (options, args) = parser.parse_args()

    main(args, options.__dict__)
    reactor.run()
