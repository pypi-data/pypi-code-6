# -*- coding: utf-8 -*-
import json

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class UserProfileView():
    """User profile information
    """
    def __call__(self):
        """Returns ITYOU ESI Parameters
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')
        
        if action == "whoami":
            return self.whoami()
        else:
            return False    

    def whoami(self):
        """Returns parameters
        """
        context  = aq_inner(self.context)
        request  = context.REQUEST
        
        if request.get("portrait_size"):
            portrait_size = request.get("portrait_size")
        else:
            portrait_size = None
        
        mt        = getToolByName(context,'portal_membership')
        auth_member = mt.getAuthenticatedMember()
        
        user_info = {
             "name"         : auth_member.getProperty("fullname") or auth_member.getId(),
             "portrait"     : mt.getPersonalPortrait(auth_member.getId(), size=portrait_size).absolute_url(),
             "user_id"      : auth_member.getId()
             }
        
        ju = JsonApiUtils()
        return ju._json_response( context,  user_info )
   
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