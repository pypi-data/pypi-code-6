
import time
import redis

from rated import settings
from .base import RateLimitBackend

# Connection pool
POOL = redis.ConnectionPool(**settings.REDIS)

class RedisBackend(RateLimitBackend):

    def do_check_realm(self, source, realm, conf):
        key = 'rated:%s:%s' % (realm, source,)
        now = time.time()

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        # We don't need these to operate in a transaction, as none of the values
        # we send are dependant on values in the DB
        pipe = client.pipeline(transaction=False)
        # Add our timestamp to the range
        pipe.zadd(key, now, now)
        # Update to not expire for another DURATION
        pipe.expireat(key, int(now + conf.get('duration', settings.DEFAULT_DURATION)))
        # Remove old values
        pipe.zremrangebyscore(key, '-inf', now - conf.get('duration', settings.DEFAULT_DURATION))
        # Test count
        pipe.zcard(key)
        size = pipe.execute()[-1]
        return size > conf.get('limit', settings.DEFAULT_LIMIT)
