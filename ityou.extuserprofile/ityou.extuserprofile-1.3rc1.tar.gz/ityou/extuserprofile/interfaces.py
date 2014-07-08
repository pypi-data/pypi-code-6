#-*- coding: utf-8 -*-
from z3c.form import interfaces
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('ityou.extuserprofile')

class IExtUserProfileSettings(Interface):
    """Global userprofile settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    extuserprofile_enabled = schema.Bool(
            title=_(u"Enable user list"),
            description=_(u"You can enable here the user list in place of the Members folder."),
            required=False,
            default=False,
        )
    
class IExtUserProfile(Interface):
    """Marker interface
    """
