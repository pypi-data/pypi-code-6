from zope.interface import Interface

from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('ityou.esi.theme')


class IESIThemeSettings(Interface):
    """Global settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    statusflag_period = schema.Int(
            title=_(u"Time period for ajax requests"),
            description=_(u"Enter the time period between two Ajax-Requests."),
            required=True,
            default=5,
        )

    #postgresql_string = schema.TextLine(
    #        title=_(u"Connection string of postgresql database"),
    #        description=_(u"Enter the connection string of postgresql database."),
    #        required=False,
    #        default=u"postgresql+psycopg2://<DB-USER>:<DB-USERPASSWORD>@localhost/ityou_esi"
    #    )


class IESITheme(Interface):
 """Marker Interface
 """
