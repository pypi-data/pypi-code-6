# -*- coding: utf-8 -*-
from datetime import date, timedelta
import logging
import json
import time 
from Acquisition import aq_inner

from zope.interface import implements
from zope.component.hooks import getSite

from plone.memoize import view
#from plone.memoize.instance import memoize
from plone.outputfilters.browser.resolveuid import uuidToObject, uuidFor
from plone.memoize import forever

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from .. import _
from . import TRANSLATION 

from ..config import IMG_TAG, LAST_LOGIN_STRING, DEFAULT_START_DATE

from ..dbapi import DBApi
db = DBApi()
ext_properties = db.getExtendedProfileProperties()



class  AjaxUsersView(BrowserView):
    """ Funktion wird durch form_send_user_search aufgerufen
        ueberprueft ob User gesucht werden sollen
    """

    def __call__(self):
        """This view is called when userproles are loaded in datatables
        """
        self.request.set('disable_border', True)        

        context = aq_inner(self.context)
        request = context.REQUEST
        group   = request.get('g','')
        raw     = request.get('raw', False)
        return self._group_users(group, raw)

    ##@view.memoize    
    def _group_users(self, qgroup=None, raw=False):
        """ ueberprueft alle Benutzer bzw. deren Informationen nach dem Suchbegriff,
            erstellt fuer passende User Dictionaries und speichert diese in einer Liste
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context, 'portal_membership') 
        ut      = Utils()
        
        # check parameters, the javascript returns
        if raw: raw = True
        if qgroup == 'undefined': qgroup = ''        
        
        group_users = mt.searchForMembers( {"groupname" : qgroup}  )

        users = []
        for group_user in group_users:
            user_id     = group_user.getId()
            u           = mt.getMemberById(user_id)
            uid         = u.getId().decode('utf-8')
            eup         = db.getExtendedProfile(uid)

            user_fullname   = ut._fomated_user_name(u,eup)
            user_last_login = ut._convert_time(u.getProperty("login_time"), raw)
            user_phone      = eup.phone or ''
            user_portrait   = mt.getPersonalPortrait(uid, size='pico').absolute_url()

            if not raw:
                # wrapped in img tag
                user_portrait   = IMG_TAG % (user_portrait, user_fullname)

            users.append((
                '', #LM wird zum sortieren verwendet 15.05.2014 MR
                user_portrait,
                user_fullname,
                '',
                db.getProperty(uid, "position"),
                user_phone,
                u.getProperty("location", ""),
                user_last_login,
                uid,
                ))

        result = { "iTotalRecords" : len(users),
                   "iTotalDisplayRecords": len(users),
                   "aaData": users}

        return ut.jsonResponce(context, result)



class UsersView(BrowserView):
    """This is the default view of the user listing (datatables)
    """
    html_template = ViewPageTemplateFile('templates/users.pt')
    
    def __call__(self):
        """Standard view
        """
        self.request.set('disable_border', True)
        self.request.set('action', 'userlist')
        self.site = getSite()
        self.ESI_ROOT = self.site.absolute_url() 
        return self.html_template()


    def listGroups(self):
        """Returns list of groups and omit standard groups
        """
        STANDARD_GROUPS = ['Administrators', 'Reviewers', 'Site Administrators', 'AuthenticatedUsers']

        gt = getToolByName(self, "portal_groups")
        list_all_groups = gt.listGroupIds()

        false_groups = set(STANDARD_GROUPS)
        all_groups   = set(list_all_groups)
        
        valid_groups = all_groups.difference(false_groups) 
        return valid_groups



class Utils():
    """Several Utils for data transformation
    """

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

    def _convert_time(self, dtime, raw):
        """ Konvertiert Zope-DateTime zu Datum in String-Format
            dtime: Zeitstempel mit Format 2000/01/01 00:00:00 GMT+1
            raw=True: Rohdaten als Tuple zurück geben
            raw=False: Daten als String für Datatables zurück  
        """
        if str(dtime) == DEFAULT_START_DATE:
            return ("", 0)
        else:
            return (dtime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), int(dtime.strftime("%s")))

        if str(dtime) == DEFAULT_START_DATE:
            res = (    0 , TRANSLATION["never"]     )
        else:
            date_today = date.today()
            date_yesterday = date_today - timedelta(1)
            date_login = date.fromtimestamp(dtime)
            timestamp = time.localtime(dtime.millis()/1000)
            
            if date_login == date_today:
                dtime_str = "%s, %s" % (TRANSLATION["today"], time.strftime("%H:%M", timestamp ))              
            elif date_login == date_yesterday:
                dtime_str = "%s, %s" % (TRANSLATION["yesterday"], time.strftime("%H:%M", timestamp))
            else:
                dtime_str = time.strftime("%d.%m.%y, %H:%M", timestamp)                
            res = (int(dtime.strftime("%s")), dtime_str)
            
        if raw:
            return res
        else:
            return LAST_LOGIN_STRING  % res
    
    def _fomated_user_name(self, u, eup):
        """Returns user name = Acad + firstname + Lastname
        if available 
        """
        user_fullname = ""
        
        if eup.lastname and eup.firstname:
            at = ""
            if eup.acadtitle:
                at = "(%s)" % eup.acadtitle
            user_fullname = "%s%s, %s" % (  eup.lastname, at, eup.firstname   )
        else:
            user_fullname = u.getProperty("fullname", "")
        
        return user_fullname

