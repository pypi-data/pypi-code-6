# -*- coding: utf-8 -*-
import json

from Acquisition import aq_inner
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView

class EsiParamsView():
    """ESI Parameters
    """
    def __call__(self):
        """Returns ITYOU ESI Parameters
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')
        
        if action == "get_params":
            return self.get_params()
        else:
            return False
    
    def get_params(self):
        """Returns parameters
        """
        context  = aq_inner(self.context)
        request  = context.REQUEST
        
        #DoTo
        params = ({
                'ESI_ROOT':                 getSite().absolute_url(),    
                'WHOISONLINE_DELAY':        5000,
                'ASTREAM_ACTIVITY_DELAY':   5000,
                'ASTREAM_COMMENT_DELAY':    15000,
                'IMESSAGE_DELAY':           5000, 
            })
        
        ju = JsonApiUtils()
        return ju._json_response( context,  params   )

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