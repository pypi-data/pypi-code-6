# -*- coding: utf-8 -*-
import json
from time import time
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.memoize.instance import memoize
from plone.outputfilters.browser.resolveuid import uuidToObject, uuidFor

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

#from .. import db_astream, db_imessage, imessage_utils 
from .. import db_astream

# ------ redis ---------------------------------------
from ..dbapi import RDBApi
rdb = RDBApi()
# ------ /redis --------------------------------------

class AjaxNotifyView(BrowserView):
    
    def __call__(self):
        """
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action = request.form.get('action')
        timestamp = request.form.get('timestamp')      

        # ! javascript may send 'null'    
        if timestamp == 'null':
            timestamp = None
                
        if action == "count_latest_activities":
            return self.count_latest_activities(timestamp)
        elif action == "count_latest_comments":
            return self.count_latest_comments(timestamp)
        elif action == "latest_senders":
            return self.get_latest_senders()        
        elif action == "count_latest_messages":
            return self.count_messages()
        else:
            pass
        return None 
    
    def count_latest_activities(self,timestamp):
        """ Count altest activities 
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt = getToolByName(context, "portal_membership")
        uid = mt.getAuthenticatedMember().getId()

        # --- psql ----
        rdb.setStatus('astream', False, uid = uid)    
        # --- /psql ----

        if db_astream:
            # ==== DB =============================================================
            acts = db_astream.getActivities(timestamp=timestamp)
            # ==== /DB =============================================================
                   
            p_acts = self._permission_activities(acts)
            nu = NotifyUtils()
            return nu.jsonResponse(context, len(p_acts) )

            #self.request.response.setHeader("Content-type","application/json")
            #return json.dumps(len(p_acts))
        else:
            return False

    def count_latest_comments(self,timestamp):
        """ Count latest comments 
        """
        #ToDo
        pass

    def _permission_content(self,acts):
        """ Returns only content to the user that he/she
        is allowed to see
        """        
        return [ uuidToObject(a['id']) for a in acts ]
    
    def _permission_activities(self, acts):
        """ Display only activities wich are linked to
        documents the the user is allowed to see
        """
        return  [ a for a in acts if uuidToObject(a['id'])  ]


class AjaxStatusFlags(BrowserView):
    
    def __call__(self):
        """Returns status flags
        """
        #t1 = time()
        context =   aq_inner(self.context)
        mt =        getToolByName(context, "portal_membership")
        uid =       mt.getAuthenticatedMember().getId()
        nu =        NotifyUtils()
        
        sflags = rdb.getStates(uid)
        json_response = nu.jsonResponse(context, sflags)
        #t2 = time() - t1
        #print "DAUER @@ajax-statusflags:", t2*1000
        return json_response


class NotifyUtils():
    """small utils
    """

    def jsonResponse(self, context, data):
        """ Returns Json Data wrapped in Callback function
        """
        request = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)
    
