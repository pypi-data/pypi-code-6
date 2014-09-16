# -*- coding: utf-8 -*-
import logging
from time import time

# ------- redis -------------------------------------------
from config import WIO_USERS_KEY
from config import REDIS_SERVER
import redis
# ------- /redis ------------------------------------------

class RDBApi(object):
    """ REDIS aPI - Redis Server must be startet!
        > service redis-server start
    """
    def __init__(self):
        """Initialize Database
        """
        self.redis = redis.Redis(REDIS_SERVER)

    def getOnlineUsers(self, max_users=20):
        """Get all users in the redis db
        """
        ou = self.redis.zrange(WIO_USERS_KEY, 0, max_users, desc=True, withscores=True)
        return ou

    def setOnlineUser(self, uid):
        """Write an online user with given id to redis db
        """ 
        t1 = time()
        self.redis.zadd( WIO_USERS_KEY, uid , int(time()) )
        return True


