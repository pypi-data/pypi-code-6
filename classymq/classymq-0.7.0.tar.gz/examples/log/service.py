from classymq.service import ConsumerService
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from examples.log.consumer import LogConsumer

__author__ = 'gdoermann'


class LoggingBase(ConsumerService):
    consumer_klass = LogConsumer

@inlineCallbacks
def main(*args, **kwargs):
    logger = LoggingBase()
    yield logger.run()

if __name__ == '__main__':
    main()
    reactor.run()