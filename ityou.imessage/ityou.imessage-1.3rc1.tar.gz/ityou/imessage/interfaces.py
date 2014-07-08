#-*- coding: utf-8 -*-
from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('ityou.astream')

class IInstantMessageSettings(Interface):
    """Global instant message settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    imessage_delay = schema.Int(
            title=_(u"Time period for ajax requests"),
            description=_(u"Enter the time period between to Ajax-Requests. \
                    IMPORTANT: Be aware that time period less then 10 second may slow down your server! \
                    Time periods less then 4 seconds are not considered."),
            required=True,
            default=10,
        )


class IInstantMessage(Interface):
    """Marker Interface
    """

