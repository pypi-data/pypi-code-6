#-*- coding: utf-8 -*-

from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('ityou.thumbnails')


class IThumbnails(Interface):
    """Marker Interface
    """
    
class IThumbnailSettings(Interface):
    """Global thumbnail settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cutycapt_installed = schema.Bool(
            title=_(u"CutyCapt for Website-Thumbnails installed?"),
            description=_(u"If CutyCapt is installed, nice thumbnails of Websites are possible."),
            required=False,
            default=False,
        )