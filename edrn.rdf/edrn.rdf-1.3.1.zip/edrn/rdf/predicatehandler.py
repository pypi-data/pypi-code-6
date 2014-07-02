# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Simple Predicate Handlers.'''

from five import grok
from zope import schema
from plone.directives import form, dexterity
from edrn.rdf import _
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from Acquisition import aq_inner

class ISimplePredicateHandler(form.Schema):
    '''An abstract handler for a predicate in the simple DMCC RDF generator.'''
    title = schema.TextLine(
        title=_(u'Token Key'),
        description=_(u"Key name of the token in the DMCC's web service description."),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this RDF source.'),
        required=False,
    )
    predicateURI = schema.TextLine(
        title=_(u'Predicate URI'),
        description=_(u'URI of the predicate to use when encountering tokenized keys of this kind.'),
        required=True,
    )
    

