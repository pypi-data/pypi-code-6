# -*- coding: utf-8 -*-
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IRtMaracasLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IRtMaracasMarkedForViewlet(Interface):
    """ Marker interface to display maracas with a viewlet
    """
