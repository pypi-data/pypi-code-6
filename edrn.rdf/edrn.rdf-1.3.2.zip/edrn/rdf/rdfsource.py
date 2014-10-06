# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''RDF Source'''

from Acquisition import aq_inner
from edrn.rdf import _
from five import grok
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from rdfgenerator import IRDFGenerator
from z3c.relationfield.schema import RelationChoice
from zope import schema

class IRDFSource(model.Schema):
    '''A source of RDF data.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this RDF source'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this RDF source.'),
        required=False,
    )
    generator = RelationChoice(
        title=_(u'Generator'),
        description=_(u'Which RDF generator should this source use.'),
        required=False,
        source=ObjPathSourceBinder(object_provides=IRDFGenerator.__identifier__),
    )
    approvedFile = RelationChoice(
        title=_(u'Active RDF File'),
        description=_(u'Which of the RDF files is the active one.'),
        required=False,
        source=ObjPathSourceBinder(portal_type='File'),
    )
    active = schema.Bool(
        title=_(u'Active'),
        description=_(u'Is this source active? If so, it will have RDF routinely generated for it.'),
        required=False,
        default=False,
    )
    


class View(grok.View):
    '''RDF output from an RDF source.'''
    grok.context(IRDFSource)
    grok.require('zope2.View')
    grok.name('rdf')
    def render(self):
        context = aq_inner(self.context)
        if context.approvedFile and context.approvedFile.to_object:
            self.request.response.redirect(context.approvedFile.to_object.absolute_url())
        else:
            raise ValueError('The RDF Source at %s does not have an active RDF file to send' % '/'.join(context.getPhysicalPath()))
        
    