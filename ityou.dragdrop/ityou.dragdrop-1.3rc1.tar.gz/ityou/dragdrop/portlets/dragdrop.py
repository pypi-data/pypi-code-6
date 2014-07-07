# -*- coding: utf-8 -*-
from Acquisition import aq_inner

from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implements

from .. import _

class IDragDropPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    implements(IDragDropPortlet)
    
    title = _(u"Drag & Drop")

class Renderer(base.Renderer):
    
    _template = ViewPageTemplateFile('dragdrop.pt')
    
    def render(self):

        context = aq_inner(self.context)
        mt = getToolByName(context, 'portal_membership')
        if mt.isAnonymousUser():
            return
        try:
            self.trash_folder = mt.getAuthenticatedMember().getHomeFolder()["trash"].absolute_url()
        except:
            self.trash_folder = "#"
        if not mt.isAnonymousUser() and context.defaultView() == "thumbnail_listing":
            return self._template()
              
    @property
    def available(self):
        return True

class AddForm(base.AddForm):
    form_fields = form.Fields(IDragDropPortlet)
    label = _(u"Add Drag&Drop portlet")
    description = _(u"A portlet where you can copy or move documents by copy & paste.")

    def create(self, data):
        return Assignment()
    