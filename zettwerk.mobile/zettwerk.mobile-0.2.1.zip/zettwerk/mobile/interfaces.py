from zope.interface import Interface
from zope import schema
from zettwerk.mobile import contentMessageFactory as _


class IThemesSettings(Interface):

    themename = schema.Text(
        title=_('themename', 'Theme Name'),
        description=_('The name of the mobile theme.'),
        default=u'default',
        )
