# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase    

from datetime import datetime
from time import time

# --- import redis dbapi ------------------------
from .dbapi import RDBApi 
from ityou.esi.theme.dbapi import RDBApi as FlagRDBApi
rdb = RDBApi()
frdb = FlagRDBApi()

class OnlineTrackingViewlet(ViewletBase):
    """Checks who is online and writes log to database
    """
    
    def update(self):
        super(OnlineTrackingViewlet, self).update()
                  
        context = aq_inner(self.context)        
        mt = getToolByName(context,"portal_membership")
        user = mt.getAuthenticatedMember()

        if user.getId():
            # ==== write to redis =========
            # we write eamil to uid
            #t1 = time()

            # write to redis whoisonline            
            uid = user.getId()
            rdb.setOnlineUser(uid)

            # set redis flags
            frdb.setStatus("whoisonline", 1,  uid = uid, omit_uid = True)
                
    index =  ViewPageTemplateFile('whoisonline-tracking.pt')
