from classymq import exchanges, queues
import logging
from classymq.utils import AttrDict

__author__ = 'gdoermann'

log = logging.getLogger(__name__)

class LogMessage(AttrDict):
    def __init__(self, message, hostname=None, extras=None,):
        AttrDict.__init__(self)
        self.message = message
        self.hostname = hostname
        self.extras = extras

class LogExchange(exchanges.BaseExchange):
    KEY = "log"
    TYPE = exchanges.EXCHANGE_TYPES.TOPIC
    NOWAIT = True
    DURABLE = True

class LogQueue(queues.BaseQueue):
    KEY = "Log"
    NOWAIT = True
    DURABLE = True

class NullLogger(logging.Logger):
    def handle(self, record):
        pass

    def log(self, level, msg, *args, **kwargs):
        pass

    def _log(self, level, msg, args, exc_info=None, extra=None):
        pass

    def __init__(self, name='NullLogger', level=logging.ERROR):
        logging.Logger.__init__(self, name, level)

# The null logger is important because NO LOGGING should happen on the log reader or on the producer.
# It creates an infinite loop
null_logger = NullLogger()