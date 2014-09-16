# -*- coding: utf-8 -*-

import json

from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

class AjaxPersonalImages(BrowserView):
    """ Ajax view which returns urls of images lying
    in the personal folder of the authenticated member. 
    """
    
    def __call__(self):
        """ Ajax view which returns urls of images lying in
        the personal folder of the authenticated member. 
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context, "portal_membership")
        catalog = getToolByName(context, "portal_catalog")
        
        results = catalog(portal_type='Event')
        auth_member = mt.getAuthenticatedMember()
        folder = auth_member.getHomeFolder()

        results = catalog(portal_type='Image',
                          path={ "query": '/'.join(folder.getPhysicalPath()) })
        
        images = []
        for result in results:
            images.append({"url" : result.getURL()})
        
        return json.dumps(images)