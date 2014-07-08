# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase    


from .dbapi import DBApi
db  = DBApi()

class MessageTrackingViewlet(ViewletBase):
    """Checks if user got an new message
    """
    
    def update(self):
        super(MessageTrackingViewlet, self).update()
                  
        context = aq_inner(self.context)        
        mt = getToolByName(context,"portal_membership")
        user = mt.getAuthenticatedMember()
         
        if user.getId():
            pass