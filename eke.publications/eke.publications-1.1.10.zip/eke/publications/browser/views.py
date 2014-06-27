# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Publications: views for content types.
'''

from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eke.knowledge.browser.views import KnowledgeFolderView, KnowledgeObjectView
from eke.publications.interfaces import IPublication, IPublicationFolder

_pubMedPrefix='http://www.ncbi.nlm.nih.gov/sites/entrez?Db=pubmed&Cmd=DetailsSearch&Term='
_pubMedSuffix='%5Buid%5D'

class PublicationFolderView(KnowledgeFolderView):
    '''Default view of a publication folder.'''
    __call__ = ViewPageTemplateFile('templates/publicationfolder.pt')
    def havePublications(self):
        return len(self.publications()) > 0
    @memoize
    def publications(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IPublication.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(
            title=i.Title,
            description=i.Description,
            journal=i.journal,
            authors=i.authors,
            url=i.getURL(),
        ) for i in results]
    @memoize
    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IPublicationFolder.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]
    def getPubMedURL(self, pubMedID):
        return u'%s%s%s' % (_pubMedPrefix, pubMedID, _pubMedSuffix)


class PublicationView(KnowledgeObjectView):
    '''Default view of a publication.'''
    __call__ = ViewPageTemplateFile('templates/publication.pt')
    def pubMedURL(self):
        context = aq_inner(self.context)
        return u'%s%s%s' % (_pubMedPrefix, context.pubMedID, _pubMedSuffix)
