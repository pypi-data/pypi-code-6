# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains the sqlite database interface
"""
import os
import logging
from time import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import sessionmaker

from ityou.esi.theme import PSQL_URI
from config import TABLE_FOLLOWS

BASE = declarative_base()

class Follow(BASE):
    """ Follow Database
    uid: User Id of the follower
    fid: User Id of the following
    """
    __tablename__ = TABLE_FOLLOWS
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(Unicode)
    fid             = Column(Unicode)

class DBApi(object):
    """ DB Util
    """
    def __init__(self):
        """Initialize Database
        """
        # --- psql ----------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)

        self.session = sessionmaker(bind=engine)
        BASE.metadata.create_all(engine)
        
    def getFollowings(self, uid):
        """ Finds fids matching to the uid. This are the followings 
        of the user with uid.
        Return: list of fids
        """
        t1 = time()
        try:
            se = self.session()
            q = se.query(Follow.fid).filter(Follow.uid == uid).all()
            f = []
            for m in q:
                f.append(m[0])
        except:
            logging.error('Error while executing getFollowing')
        finally:
            se.close()

        print "\t\t\tDauer getFollowings (ms):", (time()-t1)*1000            
        return f
            
    def setFollowing(self, uid, fid, remove=False):
        """ Checks if there's an entry in DB with given uid and fid. 
        If there's none, it adds one.
        If remove=True is given, the function does the opportunity.
        Returns: True if action was successful, False if not
        """
        t1 = time()
        res = False
        try:
            se = self.session()
            q = se.query(Follow).filter(Follow.uid == uid, Follow.fid == fid)
            if not remove and not q.first():
                f = Follow(
                       uid = uid,
                       fid = fid
                       )
                se.add(f)
                se.commit()
                res = True
            elif remove and q.first():
                q.delete()
                se.commit()
                res = True
            else:
                se.close()
        except:
            logging.error('Error while executing setFollowing')
        finally:
            se.close()

        print "\t\tDauer setFollowing (ms):", (time()-t1)*1000            
        return res

            
    def getFollowers(self, fid):
        """ Given is the fid. Getting uids from DB where the fid matches. 
        This are the followers of the user (fid)
        Returns: list of uids
        """
        t = time()
        f = []

        try:
            se = self.session()
            q = se.query(Follow.uid).filter(Follow.fid == fid).all()
            for m in q:
                f.append(m[0])

        except:
            logging.error('Error while executing getFollowers')
        finally:
            se.close()

        print "\t\tDauer getFollowers (ms):", (time()-t1)*1000
        return f        

    
    def isFollowing(self, uid, fid):
        """ Checks if user with uid is following the user with fid.
        Returns: True or False 
        """
        t1 = time()
        try:
            se = self.session()
            q = se.query(Follow).filter(
                Follow.uid == uid, 
                Follow.fid == fid).first()
        except:
            logging.error('Error while executing isFollowing')
        finally:
            se.close()

        print "\t\tDauer isFollowing (ms):", (time()-t1)*1000        
        if q:
            return True
        else:
            return False

