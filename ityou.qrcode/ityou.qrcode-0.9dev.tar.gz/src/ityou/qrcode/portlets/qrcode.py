# -*- coding: utf-8 -*-
"""Define a portlet used to show grouplist. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
"""

import random

from Acquisition import aq_inner

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from ..utils import QRCodeUtils
from .. import _

##from .utils import WhoAmIUtils

class IQRCodePortlet(IPortletDataProvider):

    show_all = schema.Bool(
            title=_(u"Display QR Code"),
            description=_(u"Show the genetated QR Code"),
            required=True,
            default=True,
        )

class Assignment(base.Assignment):
    implements(IQRCodePortlet)

    def __init__(self, show_all=True):
        self.show_all = show_all

    title = _(u"QRCode")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('qrcode.pt')
    
    def render(self):

        context = aq_inner(self.context)
        mt = getToolByName(context, 'portal_membership')
        
        #if not mt.isAnonymousUser():
        return self._template()
               
    @property
    def available(self):
        return True

    def view_qrcode(self):
        """Create a new qrcode of the page
        """
        context = aq_inner(self.context)

        qru = QRCodeUtils()
        return qru.create_qrcode(context)

    def qrcode_url(self):
        """Returns URL of QR Code
        """
        context = aq_inner(self.context)

        qru = QRCodeUtils()
        return qru.qrcode_url(context)


class AddForm(base.AddForm):
    form_fields = form.Fields(IQRCodePortlet)
    label = _(u"Add QRCode portlet")
    description = _(u"This portlet displays online users.")

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IQRCodePortlet)
    label = _(u"Edit QRCode portlet")
    description = _(u"This portlet displays online users.")
    
