# -*- coding: utf-8 -*-
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName 
from Acquisition import aq_inner
from zope.component.hooks import getSite
try:
    from BeautifulSoup import BeautifulSoup as bs
except:
    from bs4 import BeautifulSoup as bs
    
from ..config import TIME_STRING

from .. import isProductAvailable

class InstantMessageUtils:
    
    def senders(self,context,show_all):
        """Placeholder, TODO
        """
        senders = []
        return senders
    

    def convertMessagesForTemplate(self, context, ms):
        """ Converts the message dict to what the template needs
            ms may be a list of message-obj or
            a list of tuple like (count,<message>)
        """
        messages = []
        if not ms:
            return messages
        mt       = getToolByName(context,'portal_membership')
        
        for _m in ms:
            if type(_m) == type((0,0)):
                c, m = _m[0], _m[1]
            else:
                c, m = 1, _m
                                
            sender_id         = m['sender_id']
            sender_name       = m['sender_name']
            receiver_id       = m['receiver_id']
            receiver_name     = m['receiver_name']
            
            sender_portrait   = self.getPersonalPortrait(sender_id, size='icon').absolute_url()
            receiver_portrait = self.getPersonalPortrait(receiver_id, size='icon').absolute_url()
            timestr           = m['timestamp'].strftime(TIME_STRING)
            
            m_tmpl = {
                'sender_id':        sender_id,
                'sender_name':      sender_name,
                'sender_email':     m['sender_email'],
                'sender_portrait':  sender_portrait,
                'receiver_id':      m['receiver_id'],
                'receiver_name':    m['receiver_name'],
                'receiver_email':   m['receiver_email'],
                'receiver_portrait': receiver_portrait,
                'message':          m['message'],
                'timestamp':        str(m['timestamp']),
                'timestr':          timestr,    
                'hash':             m['md5'],
                'count':            c,
                'approved':         m['approved']
            }
            messages.append(m_tmpl)
                        
        return messages

    @memoize    
    def getSmallPortrait(self,portrait,username,size="small-personal-portrait"):
        """ rermoves width and height attributes
            and adds a class to the img tag
            if jquery is rendering the image, we only need
            the src of the image
            TO BE DELETED
        """
        
        soup = bs(portrait)
        img = soup.img

        return str(img['src'])

    @memoize
    def getPersonalPortrait(self,id=None, verifyPermission=0, size=None):
        """Adapts the original getPersonalPortrait 
        If ityou.extpersonalportrait is installed, the
        patched personal portrai will be called, else the
        default
        """
        plone = getSite()
        mt = getToolByName(plone,"portal_membership")
        if isProductAvailable('ityou.extuserprofile'):
            return mt.getPersonalPortrait(id, size=size)
        else:
            return mt.getPersonalPortrait(id=id)

