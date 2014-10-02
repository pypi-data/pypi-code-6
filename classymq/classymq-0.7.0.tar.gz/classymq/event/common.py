from classymq import exchanges, queues
import logging

__author__ = 'gdoermann'

log = logging.getLogger(__name__)

class EventExchange(exchanges.BaseExchange):
    KEY="classyevent"
    TYPE=exchanges.EXCHANGE_TYPES.TOPIC
    NOWAIT=True
    DURABLE = True

class EventQueue(queues.BaseQueue):
    """
    Creates a new queue for every consumer
    """
    KEY="classyevent-{instance_uuid}"
    AUTO_DELETE=True



