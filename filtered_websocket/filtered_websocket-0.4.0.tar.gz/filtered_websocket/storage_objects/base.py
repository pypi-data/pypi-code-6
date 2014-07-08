class BaseStorageObject(object):

    def __init__(self, options, *args, **kwargs):
        self.options = options  # Namespace object
        self.storage = None

    def get(self, item):
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def add(self, key, value):
        raise NotImplementedError

    def remove(self, key, value):
        raise NotImplementedError

    @classmethod
    def parser(cls, parser):
        """
        Intended for attaching additional arguments to an ArgumentParser.
        """
        return parser


class BasePubSubStorageObject(BaseStorageObject):
    """
    Defines standard interfaces for storage objects, like redis,
    which support pubsub.
    """

    def get_client(self):
        """
        Should return a client to be used by the pubsub listener thread.
        """
        raise NotImplementedError

    def publish(self, channel, data):
        raise NotImplementedError

    @classmethod
    def get_subscriber(cls):
        """
        Return some class which inherits from:
        filtered_websocket.storage_objects.subscribers.base.BaseSubscriber
        """
        raise NotImplementedError
