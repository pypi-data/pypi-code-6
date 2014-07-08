# -*- coding: utf-8 -*-
import logging
import time
import json
import hashlib
from datetime import datetime, date, timedelta

from Acquisition import aq_inner

from zope.component.hooks import getSite
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..dbapi import DBApi
from ..config import TIME_STRING
from ..config import MIN_IMESSAGE_DELAY
from ..interfaces import IInstantMessageSettings
from .. import isProductAvailable

from plone.outputfilters.browser.resolveuid import uuidToObject, uuidFor

from stripogram import html2text
try:
    from BeautifulSoup import BeautifulSoup as bs
except:
    from bs4 import BeautifulSoup as bs


from zope.i18n import translate


class DialogOverview(BrowserView):
    """View of an Instant Message
    """

    html_template = ViewPageTemplateFile('templates/dialog-overview.pt')

    def __call__(self):
        self.request.set('disable_border', True)        
        
        self.portal = getSite()
        self.portal_url = getSite().absolute_url()

        ru =  getUtility(IRegistry)
        # *1000: transform milliseconds to seconds
        # We put this value in the Portlet DOM so that
        # jquery can fetch it
        # if value lower than MIN_IMESSAGE_DELAY,
        # we take MIN_IMESSAGE_DELAY
        self.IMESSAGE_DELAY = max([ru.forInterface(IInstantMessageSettings).imessage_delay*1000, MIN_IMESSAGE_DELAY])
        self.ESI_ROOT = self.portal_url
        
        return self.html_template()


