# -*- coding: utf-8 -*-
import logging
import os

# -- sqlalchemy ------------------
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Unicode, UnicodeText, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import desc, and_,  or_, not_, func
from sqlalchemy.orm import sessionmaker, exc
# fuer mysql/psql
from sqlalchemy import String, Text
# -- /sqlalchemy ------------------

############Base = declarative_base()


from zope.component.hooks import getSite
from datetime import datetime, date
from time import time
from Products.CMFCore.utils import getToolByName

from config import DB_LOCATION, DB, TABLE, FULLNAME_PROPERTIES
from . import _
from userschema import Base, ExtendedUserProfile

# --- psql ---------------
from config import PSQL_URI
# --- /psql ---------------


class DBApi(object):
    """ DB Util
    """
    
    def __init__(self):
        """Initialize Database
        """
        ## --- psql ----------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)
        ## --- /psql ----------------------

        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)


    def getExtendedProfileProperties(self ):
        """ get a List of all extended Properties
        We need this to differ between standard user profile and extended 
        """
        t1 = time()
        eup = ExtendedUserProfile()
        extended_properties = [p for p in dir(eup) if p[0] != '_']
        print "\t\tDAUER:   getExtendedProfileProperties (ms):", (time()-t1)*1000            
        return extended_properties
        
    def getProperty(self, uid, prop):
        """Returns the extended user property, stored in the sql-Database
        """
        t1 = time()
        try:
            se = self.Session()
            q = se.query(ExtendedUserProfile)
            q = q.filter(ExtendedUserProfile.id == uid).one()
        except exc.NoResultFound:
            logging.warn('Could not get Extended Property of %s' % uid )
            return None
        except:
            logging.error('Error while excecuting getProperty' )
            return None
        finally:
            se.close()
            
        print "\t\tDAUER:   getProperty (ms):", (time()-t1)*1000       
        return getattr(q, prop)

    
    def setProperty(self, uid, pid, pval):
        """Sets extend user property
        """
        t1 = time()
        se = self.Session()
        property = ''
        try:
            # try if user is in db
            e = se.query(ExtendedUserProfile).filter(ExtendedUserProfile.id == uid).one()
            if hasattr(e,pid):
                if pid == "birthdate":
                    date_items = pval.split(".")
                    pval = date(int(date_items[2]), int(date_items[1]), int(date_items[0]))
                e.__setattr__(pid, pval)
                se.commit()
        except exc.NoResultFound:
            # uid not fould in db - create new user
            eup = ExtendedUserProfile()
            eup.id = uid
            if hasattr(eup,pid):
                eup.__setattr__(pid, pval)
            se.add(eup)
            se.commit()
        except: 
            logging.warn("Could not set property %s for user %s" % (pid,uid))
        finally:
            se.close()

        print "\t\tDAUER:   setProperty (ms):", (time()-t1)*1000            
        return property        
    
    def getExtendedProfile(self, uid):
        """Returns the extended user properties, stored in the sql-Database
        """
        t1 = time()
        se = self.Session()
        q = None
        try:
            q = se.query(ExtendedUserProfile)
            q = q.filter(ExtendedUserProfile.id == uid).one()    
        except exc.NoResultFound:
            return ExtendedUserProfile()
        except:
            logging.error('Error while executing getExtendedProfile')
        finally:    
            se.close()

        print "\t\tDAUER:   getExtendedProfile (ms):", (time()-t1)*1000            
        return q        
        ###return ExtendedUserProfile()
    
    def setExtendedProfile(self, uid, **props):
        """Set the extended user properties, stored in the sql-Database
        uid = userid
        if no extended
        """
        t1 = time()
        try:
            # try if user is in db
            se = self.Session()
            e = se.query(ExtendedUserProfile).filter(ExtendedUserProfile.id == uid).one()
            for p in props.keys():
                if hasattr(e,p):
                    if p == "birthdate" and str(type(props[p])) == "<type 'str'>":
                        if props[p] == "":
                            continue
                        date_items = props[p].split("-")
                        props[p] = date(int(date_items[0]), int(date_items[1]), int(date_items[2]))

                    e.__setattr__(p, props[p])                    
                    
            se.commit()
        except exc.NoResultFound:
            # uid not fould in db - create new user
            eup = ExtendedUserProfile()
            eup.id = uid
            for p in props.keys():
                if hasattr(eup,p):
                    if p == "birthdate" and (str(type(props[p])) == "<type 'str'>" or props[p] == ""):
                        if props[p] == "":
                            continue
                        date_items = props[p].split("-")
                        props[p] = date(int(date_items[0]), int(date_items[1]), int(date_items[2]))
                    eup.__setattr__(p, props[p])
            se.add(eup)
            se.commit()
        except:
            logging.warn("Could not add new user %s" % uid)
        finally:
            se.close()

        print "\t\tDAUER:   setExtendedProfile (ms):", (time()-t1)*1000            
        
    def deleteExtendedProfile(self, uid):
        """ Deletes Profile of user
        """
        se = self.Session()
        #try:
        se.query(ExtendedUserProfile).filter(ExtendedUserProfile.id == uid).delete()
        se.commit()
        se.close()
        #except:
        #    logging.error("Couldn't delete User Profile of %s" % uid)
        return True
            
