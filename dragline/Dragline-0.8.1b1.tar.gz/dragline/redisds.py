import redis


class Queue(object):

    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', serializer=None,
                 **redis_kwargs):
        """
        The default parameters are:
            namespace='queue', serializer=None, hash_func=usha1
            host='localhost', port=6379, db=0
        """
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)
        self.serializer = serializer

    def __len__(self):
        return self.qsize()

    def clear(self):
        """Deletes a list"""
        self.__db.delete(self.key)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        if self.serializer:
            item = self.serializer.dumps(item)
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
            if self.serializer:
                item = self.serializer.loads(item)
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


class Set(object):

    "A simple set with redis backend"

    def __init__(self, name, namespace='set', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def __len__(self):
        "returns the size of set"
        return self.__db.scard(self.key)

    def empty(self):
        "check whether the set is empty"
        return len(self) == 0

    def add(self, item):
        "Add an item to the set"
        self.__db.sadd(self.key, item)

    def __contains__(self, item):
        return self.is_member(item)

    def is_member(self, item):
        "Checks whtether a item is present in a set"
        return self.__db.sismember(self.key, item)

    def remove(self, item):
        "Remove an element from set"
        self.__db.srem(self.key, item)

    def clear(self):
        """Delete set"""
        self.__db.delete(self.key)


class Counter(object):
    def __init__(self, name, value=None, namespace='counter', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)
        if value is not None:
            self.set(value)

    def inc(self, value=1):
        self.__db.incr(self.key, value)

    def decr(self, value=1):
        self.__db.decr(self.key, value)

    def set(self, value):
        self.__db.set(self.key, value)

    def get(self):
        value = self.__db.get(self.key)
        if value is None:
            return 0
        else:
            return int(value)
