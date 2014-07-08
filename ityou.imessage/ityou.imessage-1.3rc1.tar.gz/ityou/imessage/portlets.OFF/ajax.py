# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName 
from Acquisition import aq_inner
from zope.component.hooks import getSite

from datetime import datetime, timedelta, date
import logging

from operator import itemgetter
from plone.memoize.instance import memoize

from ..dbapi import DBApi
from utils import InstantMessageUtils

from ..config import TIMEOUT

db  = DBApi()
mu = InstantMessageUtils()

class UserProfile():
    """Define the user profile
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

    
class AjaxInstantMessagePortletView(BrowserView):
    """AJAX list of online users 
    """
    
    template = ViewPageTemplateFile('imessage-ajax.pt')
    
    def __call__(self):
        context = aq_inner(self.context)
        request = context.REQUEST
        request.set('disable_border', True)
        return self.template()

    def get_latest_senders(self):
        """ Returns the latest message of all senders
        slm: senders_latest_message
        """        
        slm = []
        context = aq_inner(self.context)
        mt	    = getToolByName(context,'portal_membership')
        user_id	= mt.getAuthenticatedMember().getId()
        
        if user_id:
            slm = db.getMessages(receiver_ids=[user_id], group_field="sender_id", omit_sender=user_id, auth_user_id = user_id)
            slm = mu.convertMessagesForTemplate(context, slm)
            return slm
        else:
            return None
        
    def get_sender_latest_messages(self,sender_id):
        """ Returns the latest message and the amount of 
        open messages of all senders
        slm: senders_latest_message
        """
        slm = []
        
        context = aq_inner(self.context)
        mt        = getToolByName(context,'portal_membership')
        user_id    = mt.getAuthenticatedMember().getId()
        
        if user_id:
            #slm = db.getMessages(receiver_ids=[user_id],sender_id=sender_id) #BUG ############### auth_user_id fehlt!
            slm = db.getMessages(receiver_ids=[user_id],sender_id=sender_id, auth_user_id = user_id) 
            slm = mu.convertMessagesForTemplate(context, slm)
                        
            return slm
        else:
            return None
        
    def clip(self, message, count):
        """ Clip string, count words
        """
        ml = message.split(' ')
        
        if len(ml) > count:
            message = " ".join(ml[:count]) + " (...)"
        else:
            message = " ".join(ml)
        
        return message
