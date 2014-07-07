class BaseStorageObject(object):

    def __init__(self, options, *args, **kwargs):
        self.options = options  # argparse options
        self.storage = None

    def get(self, item):
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def add(self, key, value):
        raise NotImplementedError

    def remove(self, key, value):
        raise NotImplementedError


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
    def get_pubsub_listener(cls):
        """
        Return some class which implements a 'listener' method.
        All listeners should take a an opt
        """
        raise NotImplementedError
