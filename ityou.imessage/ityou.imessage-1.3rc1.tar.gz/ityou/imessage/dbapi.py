# -*- coding: utf-8 -*-
from time import time
import os
import logging
import hashlib
from datetime import datetime 
from zope.component.hooks import getSite

# --- sqlite3 --------
from config import DB_LOCATION, DB
# --- /sqlite3 --------

# --- psql ---------------
from config import PSQL_URI
# --- /psql ---------------

from config import DEBUG, USER_ID_BLACKLIST

# --- sqlalchemy -----
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Unicode, UnicodeText, Boolean
from sqlalchemy import desc, and_,  or_, not_, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

# fuer mysql/psql
from sqlalchemy import String, Text
from config import TABLE_MESSAGES, TABLE_MESSAGE_FLAGS, TABLE_MESSAGE_GROUPS

Base = declarative_base()


class Message(Base):
    """ An message Object
    """
    __tablename__ = TABLE_MESSAGES

    # --- psql --------------------------    
    id              = Column(Integer, primary_key=True)
    md5             = Column(String, unique=True)
    sender_id       = Column(Unicode)
    sender_name     = Column(Unicode)
    sender_email    = Column(Unicode)
    receiver_id     = Column(Unicode)
    receiver_name   = Column(Unicode)
    receiver_email  = Column(Unicode)
    message         = Column(UnicodeText)
    timestamp       = Column(DateTime)
    flags   = relationship("MessageFlag")
    # --- /psql --------------------------
   
class MessageGroup(Base):
    """ An message group Object
    """
    __tablename__ = TABLE_MESSAGE_GROUPS
    
    # --- psql --------------------------
    id              = Column(Integer, primary_key=True)
    group_hash      = Column(Unicode)
    group_name      = Column(Unicode)
    receiver_id     = Column(Unicode)
    # --- /psql --------------------------

class MessageFlag(Base):
    """ An message flag Object
    """
    __tablename__ = TABLE_MESSAGE_FLAGS
    
    # --- psql --------------------------
    id              = Column(Integer, primary_key=True)
    message_md5     = Column(String, ForeignKey(  TABLE_MESSAGES + '.md5' ))
    user_id         = Column(Unicode)
    hide            = Column(Boolean)
    approved        = Column(Boolean)
    deleted         = Column(Boolean)
    message = relationship("Message", backref=backref(TABLE_MESSAGE_FLAGS, order_by=id))
    # --- /psql --------------------------

class DBApi(object):
    """ DB Api to sqlite3
    """
    
    def __init__(self):
        """Initialize Database
        """

        ## --- psql ----------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)
        ## --- /psql ----------------------

        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.db_utils = DBUtils()


    def countNewMessages(self, receiver_id=None, sender_id=None, \
                    timestamp=None, approved=True):
        """ count messages
        """
        count = 0
        try:
            se = self.Session()
            q = se.query(Message.id).filter(Message.hide == None)
            if receiver_id:
                q = q.filter(Message.receiver_id == receiver_id)
                
            if sender_id:
                q = q.filter(Message.sender_id == sender_id)
                
            if timestamp:
                q = q.filter(Message.timestamp > timestamp)
                    
            count = q.count()

        except:
            logging.error('Error while executing countNewMessages')
        finally:            
            se.close()

        return count


    def getMessages(self, receiver_ids=None, sender_id=None, \
                    timestamp=None, newer=False, group_field=None, \
                    order_field="id", reverse_order=True, \
                    approved=False, omit_sender=False, max=20,offset=0, auth_user_id=None, dialog=False):
        """ get the messages of a givern receiver
        of if no receiver is passed: return all
        messages

        """

        #print "----------- getMessages params --------------------"
        #print "receiver_ids   ", receiver_ids
        #print "sender_id      ", sender_id
        #print "timestamp      ", timestamp
        #print "newer          ", newer
        #print "group_field    ", group_field
        #print "order_field    ", order_field
        #print "approved       ", approved
        #print "omit_sender    ", omit_sender
        #print "max            ", max
        #print "offset         ", offset
        #print "auth_user_id   ", auth_user_id
        #print "---------------------------------------------------"

        t1 = time()
        messages = None
        res = []

        if max > 50: max = 50 # never > 50 !

        try:        
            se = self.Session()

            if group_field:
                q = se.query( func.count(Message.id), Message, MessageFlag).outerjoin( MessageFlag, and_(MessageFlag.message_md5 == Message.md5, MessageFlag.user_id == auth_user_id) )
                """select * from messages ....
                """
            else:
                q = se.query(Message, MessageFlag).outerjoin(MessageFlag, and_(MessageFlag.message_md5 == Message.md5, MessageFlag.user_id == auth_user_id))
            
            if approved == "true":
                q = q.filter(or_(MessageFlag.approved == True, MessageFlag.approved == None, MessageFlag.user_id == None))
            elif approved == "all":
                pass
            else:
                q = q.filter(or_(MessageFlag.approved == False, MessageFlag.approved == None, MessageFlag.user_id == None))

            if receiver_ids and dialog:
                q = q.filter(or_(MessageFlag.hide == False, MessageFlag.hide == None, MessageFlag.user_id == None), or_(Message.receiver_id.in_(receiver_ids), Message.sender_id.in_(receiver_ids)))

            if receiver_ids and not dialog:
                q = q.filter(or_(MessageFlag.hide == False, MessageFlag.hide == None, MessageFlag.user_id == None), Message.receiver_id.in_(receiver_ids))

            if sender_id:
                q = q.filter(or_(MessageFlag.hide == False, MessageFlag.hide == None, MessageFlag.user_id == None), Message.sender_id == sender_id)

            if timestamp:
                if newer:
                    q = q.filter(Message.timestamp > timestamp)
                else:
                    q = q.filter(Message.timestamp < timestamp)
                    
            if omit_sender:
                q = q.filter( Message.sender_id != omit_sender)

            if order_field:
                if reverse_order:
                    q = q.order_by(desc(getattr(Message,order_field)))
                else:
                    q = q.order_by(getattr(Message,order_field))

            if group_field:
                q = q.group_by(group_field, Message.id, MessageFlag.id)

            messages = q[offset:offset+max]
            
            if group_field:
                res =  [  (message[0], self.db_utils.convertAttributesToDict(message[1], message[2]) ) for message in messages  ]
                print "\t\tDAUER getMessages (group_field) (ms):", (time()-t1)*1000            
            else:      
                res = [  self.db_utils.convertAttributesToDict(message[0], message[1])  for message in messages  ]
                print "\t\tDAUER getMessages (ms):", (time()-t1)*1000

        except:
            logging.error('Error while executing getMessages')
        finally:            
            se.close()

        return res


    def getMessage(self, md5):
        """ get amessage with a given md5 key
        """        
        message = None
        t1 = time()
        try:
            se = self.Session()
            message = se.query(Message).filter(Message.md5 == md5).one()        
        except:
            logging.error("Retrieving message %s not possible" % md5)            
        finally:
            se.close()
        
        if message:
            res = self.db_utils.convertAttributesToDict(message, None)
            print "\t\tDAUER getMessage (ms):", (time() - t1)*1000
            return res
        else:
            return False
        

    def addMessage(self,nm):
        """ Add a message to the database
            nm: New Message
        """
        t1 = time()
               
        md5 = hashlib.new('md5', str(nm) + str(datetime.now())).hexdigest()            
        timestamp = datetime.now()
         
        m = Message(
            md5             = md5,
            sender_id       = nm['sender_id'],
            sender_name     = nm['sender_name'],
            sender_email    = nm['sender_email'],
            receiver_id     = nm['receiver_id'],
            receiver_name   = nm['receiver_name'],
            receiver_email  = nm['receiver_email'],
            message         = nm['message'],
            timestamp       = timestamp
            )
        try:
            se = self.Session()
            se.add(m)
            se.commit()
        except:
            logging.error("Could not insert message %s" % str(m))
            return False
        finally:
            se.close()
            
        print "\t\tDAUER addMessage (ms):", (time()-t1)*1000
        return { 'md5':md5, 'timestamp': timestamp }


    def setMessageState(self,receiver_id,mids,state):
        """ Set the state of a message: delete or read
            possible states:
                - approved: message is approved by receiver
                - deleted: message is deleted by receiver
                - hide: hided the message
        """
        #timestamp = datetime.now()
        t1 = time()

        for md5 in mids:
            try:
                se = self.Session()
                mf = se.query(MessageFlag)
                mf = mf.filter(MessageFlag.message_md5 == md5)
                mf = mf.filter(MessageFlag.user_id == receiver_id)
                if len(mf.all()) == 0:
                    new_mf = MessageFlag(message_md5 = md5,
                                          user_id = receiver_id,
                                          hide = False,
                                          approved = False,
                                          deleted = False)
                    se.add(new_mf)
                    se.commit()
                    se.close()
                    se = self.Session()
                    mf = se.query(MessageFlag).filter(MessageFlag.message_md5 == md5)
                    mf = mf.filter(MessageFlag.user_id == receiver_id).one()
                else:
                    mf = mf.one()
                if state == "approved":
                    mf.approved = True
                elif state == "deleted":
                    mf.deleted = True
                elif state == "hide_receiver":
                    mf.hide = True
                elif state == "hide_sender":
                    mf.hide = True
                else:
                    logging.warning("setMessageState: '%s' is not a valid state" % state)
                    
                #m.timestamp = timestamp # Warum???
                se.commit()         
            except:
                logging.error("Could not '%s' message" % state)
            finally:
                se.close()        

        print "\t\tDAUER getMessageStatus (ms):", (time()-t1)*1000
        return 
        
    def updateMessage(self, md5, nm, receiver_id):
        """ Updates a message wit a given md5 in the database
            nm: New Message, 
            returns the updated text-message
        """
        message = None
        timestamp = datetime.now()
            
        try:
            se = self.Session()
            m = se.query(Message).filter(Message.md5 == md5).one()
            mfs = se.query(MessageFlag).filter(MessageFlag.message_md5 == md5, MessageFlag.user_id == receiver_id).all()
            for mf in mfs:
                mf.hide = False
                mf.approved = False
                mf.deleted = False
            message = m.message + '<br />' + nm
            m.message = message
            m.timestamp = timestamp
            se.commit()
        except:
            logging.error("Could not update Comment" )
        finally:
            se.close()

        return { 'md5':md5, 'timestamp': timestamp }
    

    def getLatestMessageOfAllSenders(self, receiver_id=None, timestamp=None, order_field="id", reverse_order=True, max=20,offset=0):
        """Returns all senders newest message 
        """
        t1 = time()
        if not receiver_id:
            return None
        
        messages = []

        try:
            se = self.Session()            
            q = se.query(Message)

            if receiver_id:
                q = q.filter(Message.receiver_id == receiver_id)
                         
            if order_field:
                if reverse_order:
                    q = q.order_by(desc(getattr(Message,order_field)))
                else:
                    q = q.order_by(getattr(Message,order_field))
                    
            if timestamp:
                if reverse_order:
                    q = q.filter(Message.timestamp > timestamp)
                else:
                    q = q.filter(Message.timestamp < timestamp)
                    
            q = q.group_by(Message.sender_id)
                    
            messages = q[offset:offset+max]
                    
        except:
            logging.error('Error while executing getLatestMessageOfAllSenders')
        finally:
            se.close()

        print "\t\tDAUER getLatestMessageOfAllSenders (ms):", (time()-t1)*1000

        if messages:
            return [  self.db_utils.convertAttributesToDict(message) for message in messages  ]
        
    
    def getDialog(self, sender_id, receiver_id, \
                        timestamp=None, newer=False, \
                        order_field="", reverse_order=False, \
                        max=20, offset=0, approved=False, auth_user_id = False):
        """ Returns the dialog between 2 members
        """
        t1 = time()
        messages = None

        try:
            se = self.Session()
            
            q = se.query(Message, MessageFlag).outerjoin(MessageFlag, and_(MessageFlag.message_md5 == Message.md5, MessageFlag.user_id == auth_user_id))
            q = q.filter(or_(and_(Message.sender_id == sender_id,Message.receiver_id == receiver_id),\
                             and_(Message.sender_id == receiver_id,Message.receiver_id == sender_id)))

            q = q.filter(or_(MessageFlag.hide == None, MessageFlag.hide == False))
            if approved == "true":
                q = q.filter(MessageFlag.approved == True)
            elif approved == "all":
                pass
            else:
                q = q.filter(or_(MessageFlag.approved == False, MessageFlag.approved == None))
            
            if timestamp:
                if newer:
                    q = q.filter(Message.timestamp > timestamp)
                else:
                    q = q.filter(Message.timestamp < timestamp)
                    
            if order_field:
                if reverse_order:
                    q = q.order_by(desc(getattr(Message,order_field)))                
                else:
                    q = q.order_by(getattr(Message,order_field))

            messages = q[offset:offset+max]
            messages.reverse()

        except:
            logging.error('Error while executing getLatestMessageOfAllSenders')        
        finally:
            se.close()

        print "\t\tDAUER getDialog (ms):", (time()-t1)*1000
        if messages:
            return [  self.db_utils.convertAttributesToDict(message[0], message[1]) for message in messages  ]

    
    def createGroup(self, receiver_ids, group_name):
        """ Creates a messaging group in database
        """
        m = hashlib.md5()
        m.update(str(receiver_ids))
        m.update(str(datetime.now()))
        hash = m.hexdigest()
        group_entries = []
        for id in receiver_ids:
            group_entries.append(MessageGroup(
                                             group_hash = m.hexdigest(),
                                             group_name = group_name,
                                             receiver_id = id
                                             ))
        try:
            se = self.Session()
            se.add_all(group_entries)
            se.commit()

        except:
            logging.error('Error while executing createGroup')        
        finally:
            se.close()
        
        return hash

    
    def getReceiversOfGroup(self, md5):
        """ Get receivers of group by hash
        """
        receiver_list = None
        try:
            se = self.Session()
            receivers = se.query(MessageGroup.receiver_id).filter(MessageGroup.group_hash == md5).all()
            receiver_list = []
            if receivers:
                for r in receivers:
                    receiver_list.append(r[0])
        except:
            logging.error('Error while executing getReceiversOfGroup')
        finally:
            se.close()

        return receiver_list

    
    def getGroupname(self, md5):
        """ Get group name for md5
        """
        res = None
        try:
            se = self.Session()
            groupname = se.query(MessageGroup.group_name).filter(MessageGroup.group_hash == md5).first()
            res = groupname[0]
        except:
            logging.error('Error while executing getGroupname')
        finally:
            se.close()

        return res

    
    def getGroupsOfUser(self, user_and_groups):
        """ Gets all imessage-groups of a user.
        Given is a list with the user_id and his groups
        """
        hash_list = []
        try:
            se = self.Session()
            hashs = se.query(MessageGroup.group_hash).filter(MessageGroup.receiver_id.in_(user_and_groups)).all()
            for hash in hashs:
                hash_list.append(hash[0])
        except:
            logging.error('Error while executing getGroupsOfUser')
        finally:
            se.close()

        return hash_list
    
    def deleteMessagesOfUser(self, uid):
        """ Deletes all messages of an user
        """
        se = self.Session()
        try:
            q = se.query(Message.md5).filter(or_(Message.receiver_id == uid, Message.sender_id == uid)).all()
            message_md5s = []
            for md5 in q:
                if not md5[0] in message_md5s:
                    message_md5s.append(md5[0])
            
            se.query(MessageFlag).filter(MessageFlag.message_md5.in_(message_md5s)).delete(synchronize_session='fetch')
            se.commit()
            se.query(Message).filter(or_(Message.receiver_id == uid, Message.sender_id == uid)).delete(synchronize_session='fetch')
            se.commit()
        except:
            logging.error("Couldn't delete messages for user %s" % uid)
        finally:
            se.close()
        
        return True

class DBUtils():
    """ Help functions / Utils
    """
    def convertAttributesToDict(self, object, object_flags):
        """Returns all public attributes of an object as a dict of attributes"""
        adict = dict((key, value) for key, value in object.__dict__.iteritems() 
                   if not callable(value) and not key.startswith('_'))
        if object_flags == None:
            adict["approved"] = False
            adict["deleted"] = False
        else:
            flagdict = dict((key, value) for key, value in object_flags.__dict__.iteritems() 
                   if not callable(value) and not key.startswith('_'))
            adict.update(flagdict)
        
        return adict
