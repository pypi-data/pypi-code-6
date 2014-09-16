# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains the interface classes of ityou.follow
"""
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('ityou.follow')

class IFollowSettings(Interface):
    """Global follow settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

class IFollow(Interface):
    """Marker Interface
    """

