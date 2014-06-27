# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Publications: RDF ingest for publication folders and their publications.
'''

from eke.knowledge.browser.rdf import IngestHandler, KnowledgeFolderIngestor, CreatedObject, registerHandler
from eke.knowledge.browser.utils import updateObject
from rdflib import URIRef
from Acquisition import aq_inner

# Well-known URI refs
_publicationTypeURI = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Publication')

class PublicationFolderIngestor(KnowledgeFolderIngestor):
    '''Publication folder ingestion.'''
    def __call__(self):
        rc = super(PublicationFolderIngestor, self).__call__()
        createdObjects, renderMode = self.objects, self.render
        self.render = False
        for url in aq_inner(self.context).additionalDataSources:
            super(PublicationFolderIngestor, self).__call__(rdfDataSource=url)
            createdObjects.extend(self.objects)
        self.objects, self.render = createdObjects, renderMode
        return rc

class PublicationHandler(IngestHandler):
    '''Handler for ``Publication`` objects.'''
    def createObjects(self, objectID, title, uri, predicates, statements, context):
        pub = context[context.invokeFactory('Publication', objectID)]
        updateObject(pub, uri, predicates)
        return [CreatedObject(pub)]

registerHandler(_publicationTypeURI, PublicationHandler())
