# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from rdflib import Graph
from rdflib.compare import isomorphic
from Acquisition import aq_inner
from edrn.rdf.interfaces import IRDFUpdater, IGraphGenerator
from edrn.rdf.rdfsource import IRDFSource
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from five import grok
from exceptions import NoGeneratorError, NoUpdateRequired, SourceNotActive
import datetime

RDF_XML_MIMETYPE = 'application/rdf+xml'

class RDFUpdater(grok.Adapter):
    '''Update RDF.  Adapts RDF Sources and updates their content with a fresh RDF file, if necessary.'''
    grok.provides(IRDFUpdater)
    grok.context(IRDFSource)
    def __init__(self, context):
        self.context = context
    def updateRDF(self):
        context = aq_inner(self.context)
        # If the RDF Source is inactive, we're done
        if not context.active:
            raise SourceNotActive(context)
        # Check if the RDF Source has an RDF Generator
        if not context.generator:
            raise NoGeneratorError(context)
        generator = context.generator.to_object
        generatorPath = '/'.join(generator.getPhysicalPath())
        # Adapt the generator to a graph generator, and get the graph in XML form.
        generator = IGraphGenerator(generator)
        graph = generator.generateGraph()
        # Is there an active file?
        if context.approvedFile:
            # Is it identical to what we just generated?
            current = Graph().parse(data=context.approvedFile.to_object.get_data())
            if isomorphic(graph, current):
                raise NoUpdateRequired(context)
        # Create a new file and set it active
        # TODO: Add validation steps here
        serialized = graph.serialize()
        timestamp = datetime.datetime.utcnow().isoformat()
        newFile = context[context.invokeFactory(
            'File',
            context.generateUniqueId('File'),
            title=u'RDF %s' % timestamp,
            description=u'Generated at %s by %s' % (timestamp, generatorPath),
            file=serialized,
        )]
        newFile.getFile().setContentType(RDF_XML_MIMETYPE)
        newFile.reindexObject()
        intIDs = getUtility(IIntIds)
        newFileID = intIDs.getId(newFile)
        context.approvedFile = RelationValue(newFileID)
        notify(ObjectModifiedEvent(context))
        
        
    
