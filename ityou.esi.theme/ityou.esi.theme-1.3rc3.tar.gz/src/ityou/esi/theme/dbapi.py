# -*- coding: utf-8 -*-
import os
import logging
from Acquisition import aq_inner
import datetime
from time import time

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

# --- sqlalchemy -----
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Unicode, UnicodeText, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from sqlalchemy import update
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# ---- /sqlalchemy --------


# ------- redis -------------------------------------------
import redis
from config import REDIS_SERVER, ZOPE_INSTANCE, ESI_FLAGS_KEY
# APPS = ['imessage', 'astream', 'whoisonline' ]
# --------------
# RDBApi wird von imessage, astream und whoisonline verwendet
# Aufrufe über:
#   ityou.astream.activity_event_handler
#   ityou.imessage.browser.imessage.py
#   ityou.whoisonline
#
# ------- /redis ------------------------------------------

class RDBApi(object):
    """ REDIS API - Redis Server must be startet!
        > service redis-server start
    """
    def __init__(self):
        """Initialize Database
        """
        self.redis = redis.Redis(REDIS_SERVER)

    def _user_reset(self, uid):
        """ Adds new user to the StatusFlags-Table
        """
        self.redis.sadd("users", uid) # returns True if new user, else False
        self.redis.delete("user:%s" % uid )
        #TODO: -> FB: Wo wird der gebraucht?
        #self.redis.hset("user:%s" % uid, "timestamp", time() )
        
        return True

    def setStatus(self, app, value, uid=False, omit_uid=False):
        """ Set status for user with uid and type (imessage, astream, ...) to status (true/false)
        """

        if not uid:
            # Dann wert bei allen usern setzen
            us = self.redis.smembers("users")
            for u in us:
                self.redis.hset("user:%s" % u, app, value)

        elif uid and omit_uid:
            # Dann bei allen ausser dem authentifizierten user
            self.redis.sadd("users", uid) # returns True if new user, else False
            us = self.redis.smembers("users")
            for u in us:
                if uid != u:
                    self.redis.hset("user:%s" % u, app, value)

        elif uid and not omit_uid:
            # dann Wert nur für den authenticated user setzen
            self.redis.sadd("users", uid) # returns True if new user, else False
            self.redis.hset("user:%s" % uid, app, value)

        else:
            return False

        return True

    def delStatus(self, app, uid):
        """Delete a status flag off an app
        """
        ###?self.redis.sadd("users", uid) # returns True if new user, else False
        self.redis.delete("user:%s" % uid, app)

    def getStates(self, uid):
        """ Gets uid and states for all users
        """
        ##??? warum?### timeout = time() - 120 # TODO
        flags = self.redis.hgetall("user:%s" % uid)
        self._user_reset(uid)
        return flags



