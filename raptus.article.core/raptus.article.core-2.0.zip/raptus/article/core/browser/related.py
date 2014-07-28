from Acquisition import aq_inner
from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.content import ContentRelatedItems
from plone.memoize.instance import memoize

from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces


class IRelated(interface.Interface):
    """ Marker interface for the related items viewlet
    """


class Component(object):
    """ Component which lists the related items of an article
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Related content')
    description = _(u'List of related content of the article.')
    image = '++resource++related.gif'
    interface = IRelated
    viewlet = 'raptus.article.related'

    def __init__(self, context):
        self.context = context


class Viewlet(ContentRelatedItems):
    """ Viewlet listing the related items of the article
    """
    index = ViewPageTemplateFile('related.pt')


class RelatedItemsViewlet(ViewletBase):
    """ Overrides the default related items viewlet for articles
    """
    def index(self):
        return ''
