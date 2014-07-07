# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from zope.component.hooks import getSite

class ShowPreview(BrowserView):
    """
    """
    
    html_template = ViewPageTemplateFile('templates/show_preview.pt')
    
    def __call__(self):
        """
        """
        context = aq_inner(self.context)
        mt = getToolByName(context, "portal_membership")
        self.edit_right = mt.checkPermission('edit', context)
        return self.html_template()