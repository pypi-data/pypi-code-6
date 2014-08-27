from z3c.form import interfaces

from zope import schema
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('uwosh.transitionbuttons')


class IButtonSettings(Interface):
    """Global settings for the transition button panel. Settings stored in the 
       Plone registry
    """
    floating = schema.Bool(title=u'Floating button box.',
                                description=u'Enable this option to make the transition button box float statically above the page',
                                required=False,
                                default=True)

    pageElement = schema.TextLine(title=u'Site element.', 
                                default=u'#portal-breadcrumbs',
                                description=u'Enter a CSS selector to attach the button box to. If floating is enabled, this \
                                option does nothing.',
                                required=False,)

    EnabledTypes = schema.List(title=_(u"Enable content types."),
                                description=u'The content types that the transition button box should appear on.',
                                value_type=schema.Choice(source=u"plone.app.vocabularies.UserFriendlyTypes"),
                                required=False,)

class IButtonConfigLayer(Interface):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """


