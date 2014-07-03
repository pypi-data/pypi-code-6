from zope import schema
from zope.interface import Interface
from z3c.form import interfaces
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.mobilethemeTwo')


class IMobilethemeTwoLayer(Interface):
    """A layer specific to medialog.mobilethemeTwo
        """


class IMobilethemeTwoSettings(form.Schema):
    """Adds settings to medialog.controlpanel
        """
    
    form.fieldset(
        'mobilethemeTwo',
                 label=_(u'MobilethemeTwo settings'),
                 fields=[
                         'scrape_base_url',
                         'scrape_url',
                         'scrape_selector',
                         'scrape_javascript',
                         'scrape_style'
                 ],
    )
                  
    scrape_base_url = schema.Tuple(
                             title=_('scrape_base_view', 'Embed these URLs (remember www if it is needed)'),
                             description=_('scrape_base_url',
                                           u'Hostnames to open in embed view'),
                             value_type=schema.URI(),
                             default=(u'http://plone.org',),
    )

    scrape_url = schema.URI(
                 title=_(u"scrape_url", default=u"Default URL if none is given"),
                 description=_(u"help_scrape_url",
                 default="")
    )

                  
    scrape_selector = schema.TextLine(
                             title=_('scrape_selector', 'IDs or classes to filer on'),
                             description=_('scrape_selector',
                                           u'Add in same order as base urls.'),
    )
    
    scrape_javascript = schema.Bool(
                 title=_(u"scrape_javascript", default=u"Security: Filter out javascript"),
                 description=_(u"help_scrape_javascript",
                  default="")
    )
                                


    scrape_style = schema.Bool(
                 title=_(u"scrape_style", default=u"Security: Filter out CSS styles"),
                 description=_(u"help_scrape_style",
                  default="")
    )

alsoProvides(IMobilethemeTwoSettings, IMedialogControlpanelSettingsProvider)
