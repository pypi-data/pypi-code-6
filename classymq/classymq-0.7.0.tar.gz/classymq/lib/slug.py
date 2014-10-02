from classymq import consumers, producers
from classymq.message import AmqpMessage

__author__ = 'gdoermann'

class SlugRequest(AmqpMessage):
    """
    A request that passes a FS event across the intranets
    """
    def __init__(self, slug=None, *args, **kwargs):
        super(SlugRequest, self).__init__(*args, **kwargs)
        self.slug = slug

class SlugConsumer(consumers.JsonMessageConsumer):
    ROUTING_KEY = "%(slug)s"
    MESSAGE_CLASS = SlugRequest

    def __init__(self, slug, key_params=None, rate=None, routing_keys=None):
        self.slug = slug
        if key_params is None: key_params = {}
        key_params.update({'slug': self.slug})
        super(SlugConsumer, self).__init__(key_params, rate, routing_keys)

class SlugProducer(producers.JsonProducer):
    ROUTING_KEY = "%(slug)s"
    CONSUMER = SlugConsumer
