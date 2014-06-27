# encoding: utf-8
# Copyright 2013 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_inner
from edrnsite.vanity import VANITY_UPDATE_KEY, BESPOKE_WELCOME, BESPOKE_OLD
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalTop, IHtmlHead
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName
import json

grok.context(IContentish)
grok.templatedir('templates')

class VanityReminderViewlet(grok.Viewlet):
    '''Viewlet that adds a jquery UI overlay to remind you to visit your vanity page.'''
    grok.viewletmanager(IPortalTop)
    def _getNag(self):
        context = aq_inner(self.context)
        smd = getToolByName(context, 'session_data_manager')
        session = smd.getSessionData(create=False)
        return session.get(VANITY_UPDATE_KEY, None) if session else None
    def needsToVisit(self):
        return self._getNag() == BESPOKE_WELCOME
    def needsToUpdate(self):
        return self._getNag() == BESPOKE_OLD
