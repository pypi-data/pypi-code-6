from datetime import timedelta


class Cache(object):
    def __init__(self, weeks=0, days=1, hours=0, **kwargs):
        self.validity = timedelta(weeks=weeks, days=days, hours=hours)
        self.initilize(**kwargs)

    def initilize(self):
        pass

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)
