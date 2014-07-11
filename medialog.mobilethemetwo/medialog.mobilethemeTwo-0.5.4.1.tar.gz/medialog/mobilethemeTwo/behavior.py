from zope import schema
#from plone.directives import dexterity
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.mobilethemeTwo')
 
class IScrape(form.Schema):
    """ Settings for scrape_view"""
    scrape_url = schema.URI(
        title = _("label_scrape_url", default=u"URL"),
        description = _("help_scrape_url",
        default="Path to content to embedd"),
        default='http://somesite.com/some/path',
    )

    scrape_selector = schema.ASCIILine(
        title = _("label_scrape_selector", default=u"Selector"),
         description = _("help_scrape_selector",
        default="An id or class to filter content on"),
           default='#content',
    )
    
#    scrape_base_url = schema.URI(
#         title = _("label_scrape_base_url", default=u"Base URL"),
#         description = _("help_scrape_base_url",
#         default="Base URL to external site"),
#          default='http://somesite.com',
#   )
    


alsoProvides(IScrape, IFormFieldProvider)

