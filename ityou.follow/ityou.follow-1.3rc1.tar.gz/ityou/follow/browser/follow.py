# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains all views of ityou.follow
"""
from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..dbapi import DBApi
from plone import api
import json

DB = DBApi()
     
class AjaxFollowView(BrowserView):
    """Ajax View which handles Follow events
    """

    def __call__(self):
        """ Checks the action given in the request and calls the 
        resulting function
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        
        action = request.get('action')
        if not action:
            res = None
        elif action == 'set_following':
            res = self.setFollowing()
        else:
            res = False
        
        return self.jsonResponse(context, res)
    
    def setFollowing(self):
        """ Checks the authenticated user id.
        Then calls the DBApi setFollowing function with the checked uid,
        fid and remove parameter from request.
        Returns the value returned by DBApi function as jSON.
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt = getToolByName(context, 'portal_membership')
        auth_member = mt.getAuthenticatedMember()
        if api.user.is_anonymous():
            return False
        uid = auth_member.getId()
        fid = request.get('fid')
        if not mt.getMemberById(fid) or uid == fid:
            return False
        remove = request.get('remove')
        if remove == "false":
            remove = False
        return DB.setFollowing(uid, fid, remove=remove)
        
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
