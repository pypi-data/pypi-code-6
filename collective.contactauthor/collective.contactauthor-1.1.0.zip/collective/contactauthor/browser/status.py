# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone.registry.interfaces import IRegistry
from collective.contactauthor.interfaces import IAuthorViewProtectionSettings
from zope.component import queryUtility


class IContactAuthorStatus(Interface):
    
    def protection_level():
        """Return the protection_level settings"""


class ContactAuthorStatus(BrowserView):
    """Just return control panel settings, for restricted python stuff"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings = None

    def _load_settings(self):
        if not self._settings:
            registry = queryUtility(IRegistry)
            self._settings = registry.forInterface(IAuthorViewProtectionSettings, check=False)

    def protection_level(self):
        self._load_settings()
        return self._settings.protection_level

