# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''A "null" RDF generator.  This is a content object (Null RDF Generator) and an adapter that, when asked to generate
a statement graph, always produces an empty graph containing no statements whatsoever.
'''

from five import grok
from interfaces import IGraphGenerator
from rdfgenerator import IRDFGenerator
import rdflib

class INullRDFGenerator(IRDFGenerator):
    '''A null RDF generator that produces no statements at all.'''
    

class NullGraphGenerator(grok.Adapter):
    '''A statement graph generator that always produces an empty graph.'''
    grok.provides(IGraphGenerator)
    grok.context(INullRDFGenerator)
    def generateGraph(self):
        '''Generate an empty graph.'''
        return rdflib.Graph()
    
