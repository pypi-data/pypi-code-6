from ubackup import settings


class Bucket(object):
    def __init__(self):
        pass

    @property
    def conf(self):
        return settings.BUCKETS[self.TYPE]

    @property
    def TYPE(self):
        raise NotImplementedError

    def push(self, stream, name, versioning=False):
        raise NotImplementedError

    def pull(self, name):
        raise NotImplementedError

    def exists(self, name):
        raise NotImplementedError
