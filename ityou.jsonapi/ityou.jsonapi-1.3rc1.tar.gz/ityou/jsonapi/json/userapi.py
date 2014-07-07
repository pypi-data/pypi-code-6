# -*- coding: utf-8 -*-
import json
import operator


from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from plone import api

# extended user profile
from ityou.extuserprofile.dbapi import DBApi
from . import DEFAULT_PLONE_GROUPS

db = DBApi()

class UserView(BrowserView):
    """Get Plone-User with ajax
        ===> returns json 
    """
    
    def __call__(self):
        """Standard Json view
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')

        if action == "query":
            return self.query()
        elif action == "groups":
            return self.group_query()
        else:
            return False

    def query(self):
        """Query Members
        """
        LIMIT     = 10000

        context   = aq_inner(self.context)
        request   = context.REQUEST

        q         = request.get('q','')
        limit     = 200      #### HOTFIX #LM 2014-05-27 ### int(request.get('l',LIMIT))
        mt        = getToolByName(context,'portal_membership')
        
        sort_on = ''
        if q:
            if q in '?*#+&@':
                users = mt.searchForMembers(name='')
                sort_on = 'lastname'
                #unsorted_users = api.user.get_users()
                #users = []
                #for uu in unsorted_users:                    
                #    eup = db.getExtendedProfile(uu.getId())
                #    print eup.acadtitle, eup.firstname, eup.lastname
                #    users.append()
            else:
                users = mt.searchForMembers(name=q)
        else:
            users = mt.listMembers()

        ju = JsonApiUtils()
        return ju._json_response( context,  self._convert_users( users[:limit], sort_on   )  )


    def group_query(self):
        """ Query groups
        """
        context   = aq_inner(self.context)
        groups = api.group.get_groups()
        group_list = []
        for group in groups:
            if group.id not in DEFAULT_PLONE_GROUPS:
                group_list.append({
                                   "id"         : group.id,
                                   "name"       : group.getGroupName(),
                                   "portrait"   : "defaultUser.png"
                                   })
        ju = JsonApiUtils()
        return ju._json_response( context,  group_list   )

    def _convert_users(self, users, sort_on):
        """Converts Memberdata = Default user profile + extended!
        """
        context  = aq_inner(self.context)        
        user_list = []
        for u in users:
            #ToDo
            uid = u.getId().decode('utf-8')
            eup = db.getExtendedProfile(uid)       
            user_list.append({
              "id":         u.getId(), 
              "name":       u.getProperty('fullname'),
              "lastname":   eup.lastname or 'ZZZZZZZ', #TODO
              "email":      u.getProperty('email'),  
              "portrait":   u.getPersonalPortrait(u.getId(),size='pico').absolute_url(),
              "phone":      eup.phone or '',
              "location":   u.getProperty("location"),
              "position":   eup.position or '',
              "last_login": context.toLocalizedTime(u.getProperty("login_time"),long_format=1),
              "last_login_timestamp": int(u.getProperty("login_time")),
              "profile_url": "author/%s" % u.getId()
            })
        if sort_on:
            user_list.sort(key=operator.itemgetter(sort_on))

        users = []
        for u in user_list:
            print u['lastname'], u['name']

        return user_list

class JsonApiUtils():
    """small utilities
    """
    def _json_response(self, context, data):
        """ Returns Json Data in Callback function
        """
        request  = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)
