# -*- coding: utf-8 -*-
import logging
import json
from time import time
from datetime import datetime, timedelta, date
from operator import itemgetter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName 
from Acquisition import aq_inner
from zope.component import getUtility
from zope.component.hooks import getSite
from plone.registry.interfaces import IRegistry
from plone.memoize.instance import memoize

from ..interfaces import IWhoIsOnlineSettings
from .. import _
from .. import db_imessage, ityou_extuserprofile_installed
from ..config import TIME_STRING

## --- sqlite3 dbapi -----------------------------
#from ..dbapi import DBApi
#db  = DBApi()

# --- import redis dbapi ------------------------
from ..dbapi import RDBApi 
rdb = RDBApi()

#TIME_STRING = _(u"%d.%m.%Y um %H:%M:%S Uhr")

class UserProfile():
    """Defines the userprofile
    """
    id          = u""                              
    fullname    = u"" 
    email       = u"" 
    profile     = u""
    home        = u""
    portrait    = u""
    recent_path = u""
    recent_doc  = u""
    recent_time = u""
    bar         = u""
    
class WhoIsOnlineAjaxView:
    """New view to handle userdata from ++++redis++++ DB
    """
    def __call__(self):
        """Returns json obj of all users who are online
        """
        t1 = time()
        online_users = []        
        context = aq_inner(self.context)
        request = context.REQUEST

        # need to calculate client time to server time difference
        time_client = float( request.get('time_client', time() ) )
        time_delta = int( time() - time_client )

        #### now user out of redis#####
        ### ru =  getUtility(IRegistry)
        ### timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online
        ### ou =  db.getOnlineUsers(timeout_online)

        ru =  getUtility(IRegistry)
        timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online

        max_users = ru.forInterface(IWhoIsOnlineSettings).max_users

        ou = rdb.getOnlineUsers(max_users) 
        if ou:
            online_users = self._convert_online_users(ou, timeout_online, time_delta)

        print "\t\tDAUER @@ajax-whoisonline (ms)", (time() - t1)*1000

        # this callback?
        wu = WhoIsOnlineUtils()
        return wu.jsonResponse(context,online_users)


    def _convert_online_users(self, online_users, timeout_online, time_delta):
        """ Converts user tuple (userid, unix timestamp)
            to the user format we need in the frontend
        """
        t1 = time()
        context = aq_inner(self.context)
                
        mt = getToolByName(context,'portal_membership')
        me = mt.getAuthenticatedMember().getId()

        users = []
        for ou in online_users:
            if (ou[0] !=  me) and ( mt.getMemberById(ou[0]) ):
                delta = time() - ou[1]
                if timeout_online > delta :
                    # bar (between 0. and 1.0)
                    bar =   round(  ( (timeout_online - delta) / timeout_online ) , 1)
                    user_data = self._get_user_data(ou[0])   
                    users.append({
                                  'id'              : ou[0],
                                  'fullname'        : user_data[2],
                                  'email'           : user_data[3],
                                  'portrait_large'  : user_data[4], 
                                  'profile'         : user_data[0],
                                  'portrait'        : user_data[1],
                                  'bar'             : bar,
                                  'recent_time'     : ou[1],
                                  'timeout_online'  : timeout_online,
                                  'time_delta'      : time_delta,
                                  })        
        return users

    @memoize
    def _get_user_data(self,uid):
        """Return user informations and keep them in cache
           does it work like this ????
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context,'portal_membership')
        user    = mt.getMemberById(uid)

        if user:
            if ityou_extuserprofile_installed:
                portrait_url = mt.getPersonalPortrait(uid, size='pico').absolute_url()
                portrait_large_url = mt.getPersonalPortrait(uid, size='large').absolute_url()
            else:
                portrait_url = mt.getPersonalPortrait(uid).absolute_url()
                portrait_large_url = portrait_url

            profile = getSite().absolute_url() + '/author/' + uid
            fullname = user.getProperty('fullname','')
            email = user.getProperty('email','')

            return profile, portrait_url, fullname, email, portrait_large_url
        else:
            logging.warn('User "%s" no longer exists' % uid)


class AjaxWhoIsOnlineView(BrowserView):
    """AJAX list of online users 
        #### ACHTUNG: Daten kommen noch aus der sqlite3
        #### wird abgeschaltet !!!
        #### Brauchen das aber noch für WhoAmI
    """
        
    template = ViewPageTemplateFile('whoisonline-ajax.pt')
    
    def __call__(self):

        context = aq_inner(self.context)
        request = context.REQUEST
        request.set('disable_border', True)
        wu = WhoIsOnlineUtils()

        action = request.get('action')
        user_id = request.get('user_id')
        
        if action == "show_userprofile":
            user_profile = self.user_profile(user_id)            
            return user_profile
        elif action == "show_onlineusers":
            online_users = self.online_users()
            return online_users        
        else:
            return self.template()

        
    #def online_users(self):
    #    """ get the short profile of users
    #    """
    #    online_users = []        
    #    context = aq_inner(self.context)
    #    request = context.REQUEST
    #
    #    ru =  getUtility(IRegistry)
    #    timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online
    #    ou =  db.getOnlineUsers(timeout_online)
    #    if ou:
    #        online_users = self._convert_online_users(ou)
    #
    #    # remote json-request?
    #    if request.get('callback',''):
    #        wu = WhoIsOnlineUtils()
    #        return wu.jsonResponse(context,online_users)
    #    else:
    #        return online_users
        
    #def user_profile(self, user_id):
    #    """ get the profile of a single user
    #    """                 
    #    user_profile = {}
    #    context = aq_inner(self.context)
    #    request = context.REQUEST
    #
    #    ru =  getUtility(IRegistry)
    #    timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online        
    #    up =  db.getUserProfile(timeout_online,user_id)
    #    if up:
    #        user_profile = self._convert_user_profile(up)
    #
    #    wu = WhoIsOnlineUtils()
    #    return wu.jsonResponse(context,user_profile)


    def _convert_user_profile(self,ou):

        context = aq_inner(self.context)
        request = context.REQUEST
                
        mt = getToolByName(context,'portal_membership')
        user_id = mt.getAuthenticatedMember().getId()
        
        ru =  getUtility(IRegistry)
        timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online
        
        user_profile = {}

        now_timestamp = int(datetime.now().strftime('%s'))
        
        if user_id !=  ou['user_id']:
            user = mt.getMemberById(ou['user_id'])

            # --- bar = 0 - 100  / auf 1.00 normiert---               
            delta = datetime.now() - ou["timestamp"]
            bar   = round(  ( float(timeout_online - delta.seconds ) / timeout_online ) , 1)
            
            image = mt.getPersonalPortrait(ou['user_id']).getTagName()
            if image != "Image":
                portrait_url = mt.getPersonalPortrait(ou['user_id']).absolute_url()
            else: # ToDo
                portrait_url = mt.getPersonalPortrait(ou['user_id']).absolute_url()

            user_fullname = user.getProperty('fullname') or user.getId()
            
            profile     = getSite().absolute_url() + '/author/' + ou['user_id'],
            home        = mt.getHomeUrl(ou['user_id'], verifyPermission=1) or profile
            
            user_profile = {
                          'id'          : ou['user_id'],                              
                          'fullname'    : user_fullname,
                          'email'       : user.getProperty('email'),
                          'profile'     : profile,
                          'home'        : home,
                          'portrait'    : portrait_url,
                          'recent_path' : ou["doc_path"],
                          'recent_doc'  : ou["doc_path"].split('/')[-1],
                          'recent_time' : ou["timestamp"].strftime(TIME_STRING),
                          'bar'         : bar
                          }
        return user_profile
        
                        
    #def _convert_online_users(self,online_users):
    #
    #    context = aq_inner(self.context)
    #    request = context.REQUEST
    #            
    #    mt = getToolByName(context,'portal_membership')
    #    user_id = mt.getAuthenticatedMember().getId()
    #
    #    ru =  getUtility(IRegistry)
    #    timeout_online = ru.forInterface(IWhoIsOnlineSettings).timeout_online
    #    max_users = ru.forInterface(IWhoIsOnlineSettings).max_users
    #
    #    users = []
    #    for ou in online_users:
    #        
    #        now_timestamp = int(datetime.now().strftime('%s'))
    #        
    #        if user_id !=  ou['user_id']:
    #
    #            user = mt.getMemberById(ou['user_id'])
    #            # --- bar = 0 - 100  / auf 1.00 normiert---               
    #            delta = datetime.now() - ou["timestamp"]
    #            bar   = round(  ( float(timeout_online - delta.seconds ) / timeout_online ) , 1)
    #            
    #            image = mt.getPersonalPortrait(ou['user_id']).getTagName()
    #            if ityou_extuserprofile_installed:
    #                portrait_url = mt.getPersonalPortrait(ou['user_id'], size='icon').absolute_url()
    #            else:
    #                portrait_url = mt.getPersonalPortrait(ou['user_id']).absolute_url()
    #            users.append({
    #                          'id'          : ou['user_id'],                              
    #                          'profile'     : getSite().absolute_url() + '/author/' + ou['user_id'],
    #                          'portrait'    : portrait_url,
    #                          'bar'         : bar
    #                          })
    #    
    #    return users[:max_users]


    def imessage_installed(self):
        if db_imessage:
            return True
        else:
            return False
    
    

#class AjaxWhoIsOnlineTrigger(BrowserView):
#    """AJAX Trgger for whoisonline 
#    """
#        
#    def __call__(self):
#        """Triggers WhoIsOnline
#        """
#        context = aq_inner(self.context)        
#        mt = getToolByName(context,"portal_membership")
#        user = mt.getAuthenticatedMember()
#         
#        if user.getId():
#            # ==== write to DB =========        
#            print "#########################"
#            db.addOnlineUser({
#               "user_id":   user.getId(),
#               "email":     user.getProperty("email",""),
#               "doc_path":  context.absolute_url()
#            })
#            
#        wu = WhoIsOnlineUtils() 
#        return wu.jsonResponse(context, { 'user_id' : user.getId()} )


class WhoIsOnlineUtils():
    """small utils"""

    def jsonResponse(self, context, data):
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

