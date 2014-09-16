# -*- coding: utf-8 -*-
import os
import logging
import hashlib
from time import time
from datetime import datetime, timedelta 
from Acquisition import aq_inner
from config import DEBUG, USER_ID_BLACKLIST

# --- sqlalchemy -------------------------------
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Unicode, UnicodeText, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

# fuer psql
from sqlalchemy import String, Text
# --- sqlalchemy -------------------------------

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from ityou.astream.interfaces import IAstreamSettings
from ityou.esi.theme.interfaces import IESIThemeSettings

from . import isProductAvailable    

# ------ redis ---------------------------------------
from ityou.esi.theme.dbapi import RDBApi
rdb = RDBApi()
# ------ /redis --------------------------------------

# --- psql -----------------------------------------------------
from ityou.esi.theme import PSQL_URI
# --- /psql -----------------------------------------------------

Base = declarative_base()

class Activity(Base):
    """ An activity Object
    """
    __tablename__ = 'activities'
    
    id              = Column(String, primary_key=True)
    content_path    = Column(Unicode)
    content_title   = Column(Unicode)
    user_id         = Column(Unicode)
    message         = Column(UnicodeText)
    comments        = relationship("Comment",backref="activities")
    timestamp       = Column(DateTime)

class Comment(Base):
    """ A Comment to the activities
    """
    __tablename__ = 'comments'
    
    id              = Column(Integer, primary_key=True)
    activity_id     = Column(String, ForeignKey('activities.id'))
    user_id         = Column(Unicode)
    comment         = Column(UnicodeText)
    timestamp       = Column(DateTime)
    revision        = Column(Integer)
    visible         = Column(Boolean)


class DBApi(object):
    """ DB Util
    """
    def __init__(self):
        """Initialize Database
        """
        ## --- psql ----------------------------------------------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)
        ## --- /psql ---------------------------------------------------------

        self.Session = sessionmaker(bind=engine)
        self.is_esi_theme_available = True #TODO #LM isProductAvailable("ityou.esi.theme")

        Base.metadata.create_all(engine)


    def getActivities(self, \
                      context=None, \
                      timestamp=None, \
                      newer=True,  \
                      order_field=None, \
                      descending=True, \
                      user_id="", \
                      content_uid=None, \
                      content_group=True, \
                      max=50, offset=0):
        """ return the latest MAX activities
        OLD: getActivityStream + getLatestActivities
        """

        #print "================================================================="
        #print "context:", context
        #print "timestamp:", timestamp
        #print "newer:", newer
        #print "order_field:", order_field
        #print "descending:", descending
        #print "user_id:", user_id
        #print "content_uid:", content_uid
        #print "content_group:", content_group
        #print "max", max
        #print "offset", offset
        #print "================================================================="

        activities = None
        if max > 50: max = 50 # never > 50 !

        if context:
            context_path ='/'.join(context.getPhysicalPath())

        activity_list = []
        try:                
            se = self.Session()
            q = se.query(Activity)
            
            if user_id:
                q = q.filter(Activity.user_id == user_id)
                
            if timestamp:
                if newer:
                    q = q.filter(Activity.timestamp > timestamp)
                else:
                    q = q.filter(Activity.timestamp < timestamp)
                    
            if context:
                q = q.filter(Activity.content_path.like( context_path + '%'  ))

            if content_uid:
                q = q.filter(Activity.id == content_uid)
                
            if order_field:
                if descending:
                    q = q.order_by(desc(getattr(Activity,order_field)))
                else:
                    q = q.order_by(getattr(Activity,order_field))
            
            #if content_group: 
            #    #ALT SQLITE## q = q.group_by(Activity.content_uid, Activity.message)
            #    q = q.group_by(Activity.id, Activity.message, Activity.id)
                        
            activities = q[offset:offset+max]

            db_utils = DBUtils()                        
            
            for activity in activities:
                comment_list = []
                comments = activity.comments

                for comment in comments:
                    comment_list.append(db_utils.convertAttributesToDict(comment))

                act =  db_utils.convertAttributesToDict(activity)
                act['comments'] = comment_list     

                activity_list.append(act)
        
        except:
            logging.error('Error while executinh getActivities')

        finally:
            se.close()
 
        return activity_list



    def countActivities(self):
        """ return the number of activities
        OLD:checkDBStatus     
        """
        amount = None

        try:
            se = self.Session()
            amount = se.query(Activity).count()

        except:
            logging.error("Counting activities not possible")

        finally:
            se.close()

        return amount 


    def addActivity(self,na):
        """ Insert an activity in the activity database
        As this method should later be used as a webservice
        the activities have to be serialized; we cannot
        use objects as parameters 
        OLD: insertActivity
        """
        #if not DEBUG and na['user_id'] not in getUtility(IRegistry).forInterface(IAstreamSettings).blacklist:
        if not DEBUG:

            a = Activity(
                id              = na['content_uid'],
                user_id         = na['user_id'],
                content_title   = na['content_title'],
                content_path    = na['content_path'],
                message         = na['message'],
                timestamp       = datetime.now()
                )

            try:
                se = self.Session()
                se.merge(a)
                se.commit()

            except:
                logging.error("Could not insert %s" % str(a))

            finally:
                se.close()
            
        return a.id


    def getActivityComments(self, activity_id, max=50, offset=0):
        """ return the latest MAX activities
        OLD: getActivityComments
        """
        
        comments = None
        
        try:
            se = self.Session()
            a = se.query(Activity).filter(Activity.id == activity_id).one()
            comments = a.comments

        except:
            logging.error("Retrieving comment wit %s not possible" % activity_id)

        finally:
            se.close()

        if comments:
            db_utils = DBUtils()                
            return [  db_utils.convertAttributesToDict(comment) for comment in comments   ]


    def getComments(self, timestamp=None, newer=True, order_field="id", descending=True, user_id="", max=50, offset=0):
        """ returns  comments
        """
        comments = None

        if max > 50: max = 50 # never > 50 !

        try:
            se = self.Session()
            q = se.query(Comment)
            if user_id:
                q = q.filter(Comment.user_id == user_id)
            if timestamp:
                if newer:
                    q = q.filter(Comment.timestamp > timestamp)
                else:
                    q = q.filter(Comment.timestamp < timestamp)
            
            if order_field and descending:
                q = q.order_by(desc(getattr(Comment,order_field)))
            comments = q.all()[offset:offset+max]

        except:
            logging.error('Error while executing getComments')

        finally:
            se.close()

        return comments


    def addComment(self,nc):
        """ Insert an comment to the activity in the database
            Comment is a dict (nc: new comment)
            nc must be a dict because this method will
            be part of a webservice
            OLD: insertActivityComment
        """
        res = {}

        timestamp = datetime.now()
        
        c = Comment(
                activity_id     = nc['activity_id'],
                user_id         = nc['user_id'],
                comment         = nc['comment'],
                timestamp       = timestamp,
                revision        = nc["revision"],
                visible         = nc["visible"]                    
                )

        try:
            se = self.Session()

            a = se.query(Activity).filter(Activity.id == c.activity_id).one()
            a.comments.append(c)

            se.commit()
            cid = c.id            
            res = { 'id':cid, 'timestamp': str(timestamp) }

        except:
            logging.error('Error while executing addComment')

        finally:
            se.close()

        return res
            
            

    def updateComment(self,id,new_comment):
        """ updates an existing comment in the database
            Comment is a dict (nc: new comment)
            nc must be a dict because this method will
            be part of a webservice
            OLD: insertActivityComment
        """
        comment = None
        res = {}
        timestamp = datetime.now()    

        try:
            se = self.Session()
            c = se.query(Comment).filter(Comment.id == id).one()
            comment = c.comment + '\n' + new_comment['comment']
            
            c.comment = comment
            c.timestamp = timestamp
            c.visible = new_comment['visible']
                    
            se.commit()            
            res = { 'id':id, 'timestamp': str(timestamp) }
        except:
            logging.error('Error while excecuting updateCommant')

        finally:
            se.close()
        
        return res
    
    def deleteComment(self, comment_id, content_uid):
        """ Deletes comment from db with comment id
        """
        try:
            se = self.Session()
            q = se.query(Comment).filter(Comment.id == comment_id, Comment.activity_id == content_uid).delete()
            se.commit()
            res = True
        except:
            logging.error('Error while excecuting deleteCommant')
            res = False
        finally:
            se.close()

        return res
    

    def activateComment(self, comment_id, content_uid):
        """ Activates comment with comment id
        """
        try:
            se = self.Session()
            c = se.query(Comment).filter(Comment.id == comment_id, Comment.activity_id == content_uid).one()
            c.visible = True
            se.commit()
            res = True
        except:
            logging.error('Error while excecuting deleteCommant')
            res = False
        finally:
            se.close()

        return res


    def deactivateComment(self, comment_id, content_uid):
        """ Activates comment with comment id
        """
        try:
            se = self.Session()
            c = se.query(Comment).filter(Comment.id == comment_id, Comment.activity_id == content_uid).one()
            c.visible = False
            se.commit()
            res = True
        except:
            logging.error('Error while excecuting deleteCommant')
            res = False
        finally:
            se.close()

        return res


    def getLatestActivityComment(self,activity_id):
        """ Returns the latest comment to the activity, if any
        """     

        if not activity_id:
            logging.warn("getLatestActivityComment: ID of the latest activity is missing.")
            return False
           
        c = None
        try:
            se = self.Session()
            a = se.query(Activity).filter(Activity.id == activity_id).one()
            c = a.comments[-1]

        except:
            logging.info("First comment to %s " % activity_id)

        finally:
            se.close()
            
        db_utils = DBUtils()

        if c:
            return db_utils.convertAttributesToDict(c)
        else:
            return False


class DBUtils():
    """ Help functions
    """        
    def convertAttributesToDict(self, object):
        """Returns all public attributes of an object as a dict of attributes"""
        adict = dict((key, value) for key, value in object.__dict__.iteritems() 
                   if not callable(value) and not key.startswith('_'))
            
        return adict

