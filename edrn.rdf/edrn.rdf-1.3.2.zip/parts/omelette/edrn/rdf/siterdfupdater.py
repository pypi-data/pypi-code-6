# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from edrn.rdf.interfaces import IRDFUpdater
from edrn.rdf.rdfsource import IRDFSource
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
import logging

_logger = logging.getLogger('edrn.rdf')

class SiteRDFUpdater(grok.View):
    '''A "view" that instructs all RDF sources to generate fresh RDF.'''
    grok.context(INavigationRoot)
    grok.name('updateRDF')
    grok.require('cmf.ManagePortal')
    def update(self):
        self.request.set('disable_border', True)
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(object_provides=IRDFSource.__identifier__)
        self.count, self.failures = 0, []
        for i in results:
            source = i.getObject()
            updater = IRDFUpdater(source)
            try:
                updater.updateRDF()
                self.count += 1
            except Exception, ex:
                _logger.exception('Failure updating RDF for "%s"', i.getPath())
                self.failures.append(dict(title=i.Title, url=source.absolute_url(), message=unicode(ex)))
        self.numFailed = len(self.failures)
