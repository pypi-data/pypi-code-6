# -*- coding: utf-8 -*-
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('collective.jazzport')


class IJazzportLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer"""


class IJazzportSettings(Interface):

    portal_types = schema.Set(
        title=_(u'Portal types'),
        description=_(u'Select downloadable portal types'),
        value_type=schema.Choice(
            title=_(u'Type'),
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'
        ),
        required=False
    )
