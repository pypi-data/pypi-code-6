# -*- coding: utf-8 -*-
import logging
import time
from Acquisition import aq_inner

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry
from plone.memoize.instance import memoize
from Products.CMFCore.interfaces._content import IFolderish


from .interfaces import IESIThemeSettings

from plone.app.layout.viewlets import common

try:
    from ityou.astream.interfaces import IAstreamSettings
except:
    logging.warn('ITYOU ASTREAM is not installed - could not load interfaces')
 

class EsiParamsViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('browser/templates/esi-params.pt')
    
    def get_template_id(self):
        """Returns the template id
        """
        context = aq_inner(self.context)    
        request = context.REQUEST
        return request.URL.split('/')[-1]

    def get_user_data(self):
        """Returns user id
        """
        #LM performance OK
        context = aq_inner(self.context)    
        mt  = getToolByName(context,"portal_membership")    
        user = mt.getAuthenticatedMember()

        udata = {}
        udata['uid'] = user.getId()
        udata['fullname'] = user.getProperty('fullname')

        homefolder = mt.getHomeFolder(udata['uid'])
        if homefolder:
            udata['homefolder'] = homefolder.absolute_url()
        else:
            udata['homefolder'] = getSite().absolute_url()
        return udata

    def get_content_uid(self):
        """ returns content UID 
        """
        context = aq_inner(self.context)    
        if not IFolderish.providedBy(context):            
            try:
                return context.UID()
            except:
                pass
        

    @memoize
    def get_comment_moderation_flag(self):
        """Returns True if comments should be moderated local/globally
        """
        return 1
    
        ru =  getUtility(IRegistry)
        mod = 0 # es wird moderiert
        try:
            comment_moderation = ru.forInterface(IAstreamSettings).comment_moderation
            if comment_moderation:
                mod = 1
        except:
            pass
        return mod

    @memoize
    def get_portal_url(self):
        """Returns portal_url
        """
        context = aq_inner(self.context)    
        portal_url = getSite().absolute_url()
        return portal_url

    @memoize    
    def get_statusflags_delay(self):
        """
        """
        ru =  getUtility(IRegistry)
        return ru.forInterface(IESIThemeSettings).statusflag_period

    @memoize
    def get_server_time_offset(self,t=None):
        """Return offset of local zone from GMT, 
        either at present or at time t.
        """

        if time.localtime(t).tm_isdst and time.daylight:
            return -time.altzone
        else:
            return -time.timezone

