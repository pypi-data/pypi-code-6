# -*- coding: utf-8 -*-

from collective.contactauthor import messageFactory as _
from zope.interface import Interface
from zope import schema


class IContactAuthorBrowserLayer(Interface):
    """Marker interface for collective.contactauthor product's layer"""


class IAuthorViewProtectionSettings(Interface):
    """Settings for the new authors page"""

    protection_level = schema.Choice(
        title=_(u"Protection level"),
        description=_('help_protection_level',
                      default=u"Security level for message system with anonymous users.\n"
                              u"Please note that opening anonymous access without captcha "
                              u"must be used only in secure contexts, like intranets."),
        required=True,
        default=u'anon-with-captcha',
        vocabulary='collective.contactauthor.vocabulary.securityLevels',
    )
