# -*- coding: utf-8 -*-

from zope import interface
from zope.app.content.interfaces import IContentType
#from plone.app.layout.navigation.interfaces import INavigationRoot

class ISubsiteRoot(interface.Interface):
    """Interface for a subsite folder"""

interface.alsoProvides(ISubsiteRoot,
                       IContentType)