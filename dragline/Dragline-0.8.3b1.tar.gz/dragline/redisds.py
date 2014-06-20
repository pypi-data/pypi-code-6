import redis

import time
import uuid

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






acquire_lua = """
local result = redis.call('SETNX', KEYS[1], ARGV[1])
if result == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return result"""


release_lua = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
"""


class Lock(object):
    def __init__(self, key, expires=60, timeout=10, **redis_kwargs):
        """Distributed locking using Redis Lua scripting for CAS operations.

        Usage::

            with Lock('my_lock'):
                print "Critical section"

        :param  expires:    We consider any existing lock older than
                            ``expires`` seconds to be invalid in order to
                            detect crashed clients. This value must be higher
                            than it takes the critical section to execute.
        :param  timeout:    If another client has already obtained the lock,
                            sleep for a maximum of ``timeout`` seconds before
                            giving up. A value of 0 means we never wait.
        :param  redis:      The redis instance to use if the default global
                            redis connection is not desired.

        """
        self.key = key
        self.timeout = timeout
        self.expires = expires
        self.redis = redis.Redis(**redis_kwargs)
        self._acquire_lua = redis.register_script(acquire_lua)
        self._release_lua = redis.register_script(release_lua)
        self.lock_key = None

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def acquire(self):
        """Acquire the lock

        :returns: Whether the lock was acquired or not
        :rtype: bool

        """
        self.lock_key = uuid.uuid4().hex
        timeout = self.timeout
        while timeout >= 0:
            if self._acquire_lua(keys=[self.key],
                                 args=[self.lock_key, self.expires]):
                return
            timeout -= 1
            if timeout >= 0:
                time.sleep(1)
        raise LockTimeout("Timeout while waiting for lock")

    def release(self):
        """Release the lock

        This only releases the lock if it matches the UUID we think it
        should have, to prevent deleting someone else's lock if we
        lagged.

        """
        if self.lock_key:
            self._release_lua(keys=[self.key], args=[self.lock_key])
        self.lock_key = None


class LockTimeout(BaseException):
    """Raised in the event a timeout occurs while waiting for a lock"""