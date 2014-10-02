import sys
import traceback
from classymq import producers
from examples.log import consumer, common

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor


class LogProducer(producers.JsonProducer):
    CONSUMER = consumer.LogConsumer

    def _log(self, msg, log_level=None, *args, **kwargs):
        pass

    def log(self, msg, log_level=None, *args, **kwargs):
        pass


@inlineCallbacks
def main():
    producer = LogProducer()
    try:
        yield producer.push_text(raw=sys.argv[1])
        yield producer.close()
    except Exception:
        traceback.print_exc()
    finally:
        yield reactor.stop()

if __name__ == "__main__":
    if not sys.argv != 2:
        print "{} content".format(sys.argv[0])
        exit(1)
    main()
    reactor.run()
