# -*- coding: utf-8 -*-
import logging
import json
import time

from datetime import datetime, date

from Acquisition import aq_inner

from zope.interface import implements
from zope.component.hooks import getSite

from plone.memoize.instance import memoize

from plone import api

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import url_unquote_plus

from AccessControl import AuthEncoding
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager

from ..config import ONKONNEKT_ADMIN, ONKONNEKT_ADMIN_PWD

#from ..userdataform import UserDataPanel
from .. import getAstream, getIMessage
from .. import activity_utils
from .. import _

from users import Utils

from ..dbapi import DBApi
from ..config import FULLNAME_PROPERTIES
from . import isProductAvailable

from ..userschema import FIELDSETS as FS
from ityou.imessage.dbapi import DBApi as imessage_DBApi
dbapi_imessage = imessage_DBApi()

from ityou.extuserprofile.dbapi import DBApi as extuserprofile_DBApi
dbapi_extuserprofile = extuserprofile_DBApi()

db = DBApi()
ext_properties = db.getExtendedProfileProperties()

class UserProfileView(BrowserView):
    """View for extended user profile 
    all fields of the template
    """

    def __call__(self):
        """Default View"""
        
        context     = aq_inner(self.context)
        request     = context.REQUEST

        # we need this to load the js
        request.set('action','userprofile')
        self.author = (len(request.traverse_subpath) > 0 \
                       and url_unquote_plus(request.traverse_subpath[0])) \
                       or request.get('author', None)
        self.action = request.get('action')
        self.site = getSite()
        self.ESI_ROOT = self.site.absolute_url() 

        # use project specific profiles 
        self.FS = FS

        self.thumbnails_installed = isProductAvailable("ityou.thumbnails")
        return self.index()
 
    def my_property(self):
        """is this the userprofile of the actual user?
        """        
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context,'portal_membership')
        
        user   = mt.getMemberById(self.author)
        auser  = mt.getAuthenticatedMember()

        return auser == user

    def user(self, uid=None, portrait_size='large'):
        """ returns the user data form Plone (getProperty)
        and extendedUserProfile
        this function may also be called from extern,
        Then self.author is None and me have to read
        the Request header!
        """
        context = aq_inner(self.context)
        request = context.REQUEST        
        mt      = getToolByName(context,'portal_membership')

        if not uid:
            try: 
                # called internally (default)
                uid = self.author
            except AttributeError:
                # called from extern
                uid = request.get('uid')
                if not uid:
                    logging.warn("NO AUTHOR / NO UID = NO RESULTS")
                    return

        u = mt.getMemberById(uid)
        if not u:
            logging.warn("NO USER = NO RESULTS")
            return

        auth_member     = mt.getAuthenticatedMember()
        auth_member_id  = auth_member.getUserName()
        uid             = u.getId().decode('utf-8')
        eup             = db.getExtendedProfile(uid)
        
        user                = {}        
        user['id']          = u.getId()
        user['homecity']    = u.getProperty('homecity', '')
        user['email']       = u.getProperty('email', '')
        user['description'] = u.getProperty('description', '')
        user['fullname']    = u.getProperty('fullname', '')
        user['location']    = u.getProperty('location', '')
        user['home_page']   = u.getProperty('home_page', '')
        user['home']        = mt.getHomeUrl(u.getId(), verifyPermission=1)
        user['portrait']    = mt.getPersonalPortrait(u.getId(), size=portrait_size).absolute_url()
        
        # extended properties
        for ep in ext_properties:
            try:
                if ep == "id":
                    continue
                ext_prop = eup.__getattribute__(ep)
                if type(ext_prop) == date:
                    try: #valueErrors bei Year <1900 !
                        user[ep] = date.strftime(ext_prop, "%d.%m.%Y")
                    except:
                        user[ep] = ext_prop
                elif ep == 'metadata': # do not import the sqlite3 database metadata
                    continue
                else:
                    user[ep] = ext_prop
            except:
                continue
        
        if not user['firstname'] and not user['lastname'] == "":
            firstname = " ".join(user["fullname"].split(" ")[0:-1])
            lastname = user["fullname"].split(" ")[-1]
            db.setProperty(user['id'], 'firstname', firstname)
            db.setProperty(user['id'], 'lastname', lastname)
            user['firstname'] = firstname
            user['lastname'] = lastname

            ##LM 2014-05-28
            #aup = AjaxUserProperty(context,request)
            #aup._updateFullname( auth_member )
        
        return user
    
    def get_activities(self, au_id=None):
        """returns latest activities of the author
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        max_a   = request.get("max_a",10) 
        mt      = getToolByName(context,'portal_membership')
        
        try:
            dbapi_astream = getAstream()
            acts = dbapi_astream.getActivities(context=context, user_id=au_id,max=max_a)
            p_acts = activity_utils._permission_activities(acts)
            activities = activity_utils.convertActivitiesForTemplate(context, p_acts)
            return activities
        except:
            return False

    def astream_installed(self):
        """ Checks if ityou.astream is installed
            Returns DBApi of astream or False
        """
        return getAstream()

    def imessage_installed(self):
        """ Checks if ityou.imessage is installed
            Returns DBApi of imessage or False
        """
        return getIMessage()
        
    def FollowInstalled(self):
        """ Test if ityou.follow is installed and functions are available
        """
        return isProductAvailable("ityou.follow")

class AjaxUserProperty(BrowserView):
    """Class to edit user profiles with jquery.jedit
       inline editing tool
    """

    def __call__(self):
        
        context = aq_inner(self.context)
        request = context.REQUEST

        action  = request.get("action")
        pid     = request.get("id")
        pval    = request.get("value",'').decode('utf-8')

        mt = getToolByName(context,'portal_membership')
        au = mt.getAuthenticatedMember()
        uid = au.getId().decode('utf-8') # we need unicode

        if pid not in ext_properties:
            # default user profile       
            if action == "set-property":
                au.setMemberProperties({pid : pval})
                # ToDo Date Formatting
                #return au.getProperty(pid)
                prop = au.getProperty(pid)
                if type(prop) == date:
                    prop = date.strftime(prop, "%d.%m.%Y")
                return self.jsonResponce(context, prop)
            elif action == "get-property":
                # ToDo Date Formatting
                #return au.getProperty(pid)
                prop = au.getProperty(pid)
                if type(prop) == date:
                    prop = date.strftime(prop, "%d.%m.%Y")
                return self.jsonResponce(context, prop)
        else:
            # extended user profile
            if action == "set-property":
                db.setProperty(uid, pid, pval)
                if pid in FULLNAME_PROPERTIES:
                    self._updateFullname(au)
                # ToDo Date Formatting               
                #return db.getProperty(uid, pid)
                prop = db.getProperty(uid, pid)
                if type(prop) == date:
                    prop = date.strftime(prop, "%d.%m.%Y")
                return self.jsonResponce(context, prop)
            elif action == "get-property":
                # ToDo Date Formatting
                #return db.getProperty(uid, pid)
                prop = db.getProperty(uid, pid)
                if type(prop) == date:
                    prop = date.strftime(prop, "%d.%m.%Y")
                return self.jsonResponce(context, prop)
    
    def _updateFullname(self, au):
        """ Updates fullname of member
        """
        uid = au.getId().decode('utf-8') # we need unicode
        user_profile = db.getExtendedProfile(uid)
        fullname = ""
        for prop in FULLNAME_PROPERTIES:
            val = user_profile.__getattribute__(prop)
            if val:
                fullname = fullname + val + " "
        fullname.strip()
        au.setMemberProperties({"fullname": fullname})


    def jsonResponce(self, context, data):
        """ Returns Json Data in Callback function
        """
        request = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)


class AjaxExtUserprofileView(BrowserView):
    """ Returns a user dict in JSON with user props and extended user props
        that can be used i.e. for the live search
    """

    def __call__(self):
        """default view
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context, 'portal_membership') 
        up      = UserProfileView(context,request)
        ut      = Utils()
        
        uid     = request.get('uid','')
        rjson   = request.get('json',False)
        user    = up.user(uid,portrait_size='icon')
        if rjson:
            return ut.jsonResponce(context, user)
        else:
            return user


class AjaxDeleteMe():
        """delete my own account!
        """
        def __call__(self):
            context = aq_inner(self.context)
            mt      = getToolByName(context, 'portal_membership') 
            ut      = getToolByName(context, 'acl_users')
            smanager = getSecurityManager()

            me = mt.getAuthenticatedMember()
            print "ME", me
            me_id = me.getId()

            try:
                # --- login as agentilo_admin -------------------------------------------------        
                auth_admin = ut.authenticate(ONKONNEKT_ADMIN, ONKONNEKT_ADMIN_PWD, self.request)
    
                if not auth_admin:
                    logging.warn('Sorry, you are not an admin - leave !')
                    return False
    
                admin = ut.getUserById(ONKONNEKT_ADMIN)
                if not hasattr(admin, 'aq_base'):
                    admin = admin.__of__(ut) # acquisition wrap the user
    
                # === Do anything the new user should be able to do ===================================
                newSecurityManager(self.request, admin)
    
                api.user.delete( user = me )
                print "OWN DELETE", me
    
                # === /Do anything the new user should be able to do ====================================
                setSecurityManager(smanager)
    
                self._delete_my_messages(me_id)
                self._delete_my_extuserprofile(me_id)
    
                return context.REQUEST.RESPONSE.redirect(getSite().absolute_url())
            except:
                logging.error('Could not delete user %s', me_id)


        def _delete_my_messages(self, me_id):
            return dbapi_imessage.deleteMessagesOfUser(me_id)

        def _delete_my_extuserprofile(self, me_id):
            return dbapi_extuserprofile.deleteExtendedProfile(me_id)


