# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''DMCC Committee RDF Generator. An RDF generator that describes EDRN committees using the DMCC's maladroit web services.
'''

from Acquisition import aq_inner
from edrn.rdf import _
from five import grok
from interfaces import IGraphGenerator
from rdfgenerator import IRDFGenerator
from rdflib.term import URIRef, Literal
from utils import parseTokens, DEFAULT_VERIFICATION_NUM
from utils import validateAccessibleURL
from utils import splitDMCCRows
from z3c.suds import get_suds_client
from zope import schema
import rdflib

# Map from DMCC inane key to name of field that contains the corresponding predicate URI in the committees SOAP operation
_committeePredicates = {
    u'committee_name': 'titlePredicateURI',
    u'committee_name_short': 'abbrevNamePredicateURI',
    u'committee_type': 'committeeTypePredicateURI'
}

# Map from ludicrous DMCC role names to the field that contains the corresponding predicate URI in the membership SOAP operation
_roleNamePredicates = {
    u'Chair': 'chairPredicateURI',
    u'Co-chair': 'coChairPredicateURI',
    u'Consultant': 'consultantPredicateURI',
    u'Member': 'memberPredicateURI'
}

class IDMCCCommitteeRDFGenerator(IRDFGenerator):
    '''DMCC Committee RDF Generator.'''
    webServiceURL = schema.TextLine(
        title=_(u'Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC SOAP web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )
    committeeOperation = schema.TextLine(
        title=_(u'Committee Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to retrieve committee information.'),
        required=True,
    )
    membershipOperation = schema.TextLine(
        title=_(u'Membership Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to retrieve information about whose in what committees.'),
        required=True,
    )
    verificationNum = schema.TextLine(
        title=_(u'Verification Number String'),
        description=_(u'Inane, vapid, and worthless parameter to pass to the operation. A default will be used if unset.'),
        required=False,
    )
    typeURI = schema.TextLine(
        title=_(u'Type URI'),
        description=_(u'Uniform Resource Identifier naming the type of committee objects described by this generator.'),
        required=True,
    )
    uriPrefix = schema.TextLine(
        title=_(u'URI Prefix'),
        description=_(u'The Uniform Resource Identifier prepended to all committees described by this generator.'),
        required=True,
    )
    personPrefix = schema.TextLine(
        title=_(u'Person URI Prefix'),
        description=_(u'The Uniform Resource Identifier prepended to people described as members of committees.'),
        required=True,
    )
    titlePredicateURI = schema.TextLine(
        title=_(u'Title Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates titles (names) of committees.'),
        required=True,
    )
    abbrevNamePredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates abbreviated names of committees.'),
        required=True,
    )
    committeeTypePredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the kinds of committees.'),
        required=True,
    )
    chairPredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the chairpeople of committees.'),
        required=True,
    )
    coChairPredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the co-chairpeople of committees.'),
        required=True,
    )
    consultantPredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates consultants to committees.'),
        required=True,
    )
    memberPredicateURI = schema.TextLine(
        title=_(u'Abbreviated Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates members of committees.'),
        required=True,
    )


class DMCCCommitteeGraphGenerator(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.provides(IGraphGenerator)
    grok.context(IDMCCCommitteeRDFGenerator)
    def generateGraph(self):
        graph = rdflib.Graph()
        context = aq_inner(self.context)
        verificationNum = context.verificationNum if context.verificationNum else DEFAULT_VERIFICATION_NUM
        client = get_suds_client(context.webServiceURL, context)
        committees = getattr(client.service, context.committeeOperation)
        members = getattr(client.service, context.membershipOperation)
        
        # Get the committees
        horribleCommittees = committees(verificationNum)
        for row in splitDMCCRows(horribleCommittees):
            subjectURI = None
            statements = {}
            for key, value in parseTokens(row):
                if key == u'Identifier' and not subjectURI:
                    subjectURI = URIRef(context.uriPrefix + value)
                    graph.add((subjectURI, rdflib.RDF.type, URIRef(context.typeURI)))
                elif key in _committeePredicates and len(value) > 0:
                    predicateURI = URIRef(getattr(context, _committeePredicates[key]))
                    statements[predicateURI] = Literal(value)
            for predicateURI, obj in statements.iteritems():
                graph.add((subjectURI, predicateURI, obj))
        
        # Get the members of the committees
        horribleMembers = members(verificationNum)
        for row in splitDMCCRows(horribleMembers):
            subjectURI = predicateURI = obj = None
            for key, value in parseTokens(row):
                if not value: continue
                if key == u'committee_identifier':
                    subjectURI = URIRef(context.uriPrefix + value)
                elif key == u'Registered_Person_Identifer':
                    obj = URIRef(context.personPrefix + value)
                elif key == u'roleName':
                    if value not in _roleNamePredicates: continue
                    predicateURI = URIRef(getattr(context, _roleNamePredicates[value]))
            if subjectURI and predicateURI and obj:
                graph.add((subjectURI, predicateURI, obj))
        
        # C'est tout.
        return graph
