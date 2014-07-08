# -*- coding: utf-8 -*-
"""
import random
from Acquisition import aq_inner

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite

from plone.registry.interfaces import IRegistry
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..config import MIN_IMESSAGE_DELAY
from ..interfaces import IInstantMessageSettings
from .. import _

from .utils import InstantMessageUtils

class IInstantMessagePortlet(IPortletDataProvider):

    count = schema.Int(
            title=_(u"Number of users to display"),
            description=_(u"Maximum number of users to show"),
            required=True,
            default=10,
        )
                       
class Assignment(base.Assignment):
    implements(IInstantMessagePortlet)

    def __init__(self, count=20):
        self.count = count

    title = _(u"Instant Messages")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('imessage.pt')
    
    def render(self):

        context = aq_inner(self.context)
        mt = getToolByName(context, 'portal_membership')
        
        ru =  getUtility(IRegistry)
        # *1000: transform milliseconds to seconds
        # We put this value in the Portlet DOM so that
        # jquery can fetch it
        # if value lower than MIN_IMESSAGE_DELAY,
        # we take MIN_IMESSAGE_DELAY
        self.IMESSAGE_DELAY = max([ru.forInterface(IInstantMessageSettings).imessage_delay*1000, MIN_IMESSAGE_DELAY])
        self.ESI_ROOT = getSite().absolute_url()
        # only show if not Anonymous    
        if not mt.isAnonymousUser():
            return self._template()
              
    @property
    def available(self):
        return True

    def senders(self):
        "Show users who send messages   #TODO "
        # extern utils; no need to restart zope on changes        
        who = InstantMessageUtils()
        limit = self.data.count
        return who.senders()[:limit]

class AddForm(base.AddForm):
    form_fields = form.Fields(IInstantMessagePortlet)
    label = _(u"Add IMessage portlet")
    description = _(u"This portlet displays users tat send messages.")

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IInstantMessagePortlet)
    label = _(u"Edit IMessage portlet")
    description = _(u"This portlet displays online users.")
"""    
