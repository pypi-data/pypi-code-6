# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains the sqlite database interface
"""
import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import sessionmaker

# --- psql -----------------------------------------------------
from ityou.esi.theme import PSQL_URI
# --- /psql -----------------------------------------------------

BASE = declarative_base()

class DragDrop(BASE):
    """ DragDrop Database
    user_id: User Id
    uid: UID of the Document
    """
    __tablename__ = 'dragdrop'
    
    id              = Column(Integer, primary_key=True)
    user_id         = Column(Unicode)
    uid             = Column(Unicode)

class DBApi(object):
    """ DB Util
    """
    def __init__(self):
        """Initialize Database
        """
        ## --- psql ----------------------------------------------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)
        ## --- /psql ---------------------------------------------------------

        self.session = sessionmaker(bind=engine)

        BASE.metadata.create_all(engine)
    
    def addObject(self, user_id, uid):
        """ Adds the object to the user's clipboard
        """
        res = ""
        try:
            se = self.session()
            q = se.query(DragDrop).filter(DragDrop.user_id == user_id, DragDrop.uid == uid)
            if not q.first():
                d = DragDrop(
                           user_id = user_id,
                           uid = uid
                           )
                se.add(d)
                se.commit()
                res = True
        except:
            logging.error('Error while excecuting dragdrop addObject')            
        finally:
            se.close()
        return res

    
    def removeObject(self, user_id, uid):
        """ Removes the object from the user's clipboard
        """

        try:
            se = self.session()
            q = se.query(DragDrop).filter(DragDrop.user_id == user_id, DragDrop.uid == uid)
            q.delete()
            se.commit()

        except:
            logging.error('Error while excecuting dragdrop removeObject') 
        finally:
            se.close()
        
        return True

        
    def getObjects(self, user_id):
        """ Get Objects for user
        """
        uids = []
        try:
            se = self.session()
            q = se.query(DragDrop.uid).filter(DragDrop.user_id == user_id)            
            for uid in q.all():
                uids.append(uid[0])
        except:
            logging.error('Error while excecuting dragdrop getObject')
        finally:
            se.close()

        return uids
        
