# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''RDF Generator'''

from five import grok
from zope import schema
from plone.directives import form, dexterity
from edrn.rdf import _

class IRDFGenerator(form.Schema):
    '''A generator of RDF'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this RDF generator.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this RDF generator.'),
        required=False,
    )

