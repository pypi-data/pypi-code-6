#-*- coding: utf-8 -*-
import logging
import os
from time import time
#from . import DB_LOCATION, DB, TABLE
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from Acquisition import aq_inner
from datetime import datetime
from . import ASTREAM, IMESSAGE

# --- sqlalchemy -----
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from sqlalchemy.sql import and_, or_
# ---- /sqlalchemy --------

# --- psql -----------------------------------------------------
from ityou.esi.theme import PSQL_URI
# --- /psql -----------------------------------------------------

Base = declarative_base()

class Notify(Base):
    """ A Mailer Object
    The Notify-Database is used for astream and
    imessage events.
    action: 'astream' or 'imessage'
    """

    __tablename__ = "notifies"

    id              = Column(Integer, primary_key=True)
    action          = Column(Unicode)
    sender_id       = Column(Unicode)
    sender_name     = Column(Unicode)
    sender_email    = Column(Unicode)
    receiver_id     = Column(Unicode)
    receiver_name   = Column(Unicode)
    receiver_email  = Column(Unicode)
    message         = Column(UnicodeText)
    content_uid     = Column(Unicode)
    content_title   = Column(Unicode)
    content_path    = Column(Unicode)
    timestamp_send  = Column(DateTime)
    timestamp_mod   = Column(DateTime)

class DBApi(object):
    """ DB Util
    """

    def __init__(self):
        """Initialize Database
        """
        ## sqlite ----------
        #engine  = create_engine(DB, encoding="utf-8")
        ## /sqlite ----------

        ## --- psql ----------------------
        engine  = create_engine(PSQL_URI, client_encoding='utf8', echo=False)
        ## --- /psql ----------------------

        self.Session = sessionmaker(bind=engine)
        
        # create dbs if not exist ----
        Base.metadata.create_all(engine)


    def addNotification(self, fields):
        """ Write notification into DB
        field = column of database
        """        
        t1 = time()
        n = Notify()
        for f in fields.keys():
            if hasattr(n,f):
                n.__setattr__(f,fields[f])
        try:
            se = self.Session()
            se.add(n)    
            se.commit()
        except:
            logging.error("Could not insert notification  %s" % str(n))
        finally:
            se.close()

        print "\t\tDAUER addNotification: ", (time() - t1) * 1000
        return True


    def getQueuedNotifications(self, action):
        """ Get all queued notifications from DB
            action: 'astream' or 'imessage'
        """
        t1 = time()
        try:
            se = self.Session()
            q = se.query(Notify)\
                .filter( and_(  Notify.timestamp_send == None,  Notify.action == action  ) )\
                .order_by(desc(Notify.timestamp_mod))\
                .group_by(Notify.content_uid, Notify.id).order_by(desc(Notify.timestamp_mod))
            notifications = q.all()
        except:
            logging.error("Retrieving notifications for action=%s not possible" % action)
            notifications = None
        finally:
            se.close()

        print "\t\tDAUER getQueuedNotification: ", (time() - t1) * 1000
        return notifications

    
    def markNotificationAsSent(self, trigger, timestamp_mod, content_uid = None):
        """  Marks notifications as send
        """
        t1 = time()
        se = self.Session()

        # which event triggered?
        if trigger == ASTREAM:
            notifications = se.query(Notify) \
                .filter(Notify.content_uid == content_uid, \
                        Notify.timestamp_send == None).all()
        elif trigger == IMESSAGE:
            notifications = se.query(Notify) \
                .filter(Notify.timestamp_mod <= timestamp_mod, \
                        Notify.timestamp_send == None).all()
        else: # future
            pass


        for n in notifications:
            n.timestamp_send = datetime.now()         
        try:
            se.commit()
        except:
            logging.info("Could not mark %s as sent" % content_uid)
            return False
        finally:
            se.close()

        print "\t\tmarkNotificationAsSent: ", (time() - t1) * 1000        
        return True

