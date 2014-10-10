# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer

class IFrontendLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       This is not developed to be directly used for layout registration, but
       all new skin layout that wanna be used in a subsites need to inherit from
       this interface.
    """
