# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''DMCC Protocol RDF Generator. An RDF generator that describes EDRN protocols using the DMCC's bungling web services.
'''

from Acquisition import aq_inner
from edrn.rdf import _
from five import grok
from interfaces import IGraphGenerator
from rdfgenerator import IRDFGenerator
from rdflib.term import URIRef, Literal
from utils import parseTokens, validateAccessibleURL, DEFAULT_VERIFICATION_NUM, splitDMCCRows
from z3c.suds import get_suds_client
from zope import schema
import rdflib

_siteRoles = {
    '1':                  'Funding Source',
    '2':                  'Discovery',
    '3':                  'Reference',
    '4':                  'Coordinating Site',
    '5':                  'Specimen Contributing Site',
    '6':                  'Specimen Storage',
    '7':                  'Analysis Lab',
    '8':                  'Statistical Services',
    '9':                  'Consultant',
    '97':                 'Other, Specify',
}

_reportingStages = {
    '1':                   'Development Stage',
    '2':                   'Funding Stage',
    '3':                   'Protocol Development Stage',
    '4':                   'Procedure Development Stage',
    '5':                   'Retrospective Sample Identification Stage',
    '6':                   'Recruitment Stage',
    '7':                   'Lab Processing Stage',
    '8':                   'Blinding Stage',
    '9':                   'Lab Analysis Stage',
    '10':                  'Publication Stage',
    '11':                  'Statistical Analysis Stage',
    '12':                  'Completed',
    '97':                  'Other, specify',
}

_fieldsOfResearch = {
    '1': 'Genomics',
    '2': 'Epigenomics',
    '3': 'Proteomics',
    '4': 'Glycomics',
    '5': 'Nanotechnology',
    '6': 'Metabolomics',
    '7': 'Hypermethylation',
    '9': 'Other, Specify',
}



class IDMCCProtocolRDFGenerator(IRDFGenerator):
    '''DMCC Protocol RDF Generator.'''
    webServiceURL = schema.TextLine(
        title=_(u'Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC SOAP web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )
    protocolOrStudyOperation = schema.TextLine(
        title=_(u'Protocol-Or-Study Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to retrieve protocol-or-study information.'),
        required=True,
    )
    edrnProtocolOperation = schema.TextLine(
        title=_(u'EDRN Protocol Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to retrieve information about EDRN protocols.'),
        required=True,
    )
    protoSiteSpecificsOperation = schema.TextLine(
        title=_(u'Protocol Site-Specifics Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to retrieve site-specific information about protocols.'),
        required=True,
    )
    protoProtoRelationshipOperation = schema.TextLine(
        title=_(u'Protocol-Protocol Relationship Operation Name'),
        description=_(u'Name of the SOAP operation to invoke in order to get information regarding protocol interrelationships.'),
        required=True,
    )
    verificationNum = schema.TextLine(
        title=_(u'Verification Number String'),
        description=_(u'Feeble, jejune, and daft parameter to pass to the operation. A default will be used if unset.'),
        required=False,
    )
    typeURI = schema.TextLine(
        title=_(u'Type URI'),
        description=_(u'Uniform Resource Identifier naming the type of protocol objects described by this generator.'),
        required=True,
    )
    siteSpecificTypeURI = schema.TextLine(
        title=_(u'Site-Specific Type URI'),
        description=_(u'Uniform Resource Identifier naming the type of protocol/site-specific objects described.'),
        required=True,
    )
    uriPrefix = schema.TextLine(
        title=_(u'URI Prefix'),
        description=_(u'The Uniform Resource Identifier prepended to all protocols described by this generator.'),
        required=True,
    )
    siteSpecURIPrefix = schema.TextLine(
        title=_(u'Site-Specific URI Prefix'),
        description=_(u'Prefix string to prepend to identifiers to generate complete URIs to site-specific information.'),
        required=True,
    )
    publicationURIPrefix = schema.TextLine(
        title=_(u'Publication URI Prefix'),
        description=_(u'Prefix string to prepend to identifiers to generate complete URIs to publications.'),
        required=True,
    )
    siteURIPrefix = schema.TextLine(
        title=_(u'Site URI Prefix'),
        description=_(u'Prefix string to prepend to identifiers to generate complete URIs to sites.'),
        required=True,
    )
    titleURI = schema.TextLine(
        title=_(u'Title URI'),
        description=_(u'Uniform Resource Identifier for the title predicate.'),
        required=True,
    )
    abstractURI = schema.TextLine(
        title=_(u'Abstract URI'),
        description=_(u'Uniform Resource Identifier for the abstract predicate.'),
        required=True,
    )
    involvedInvestigatorSiteURI = schema.TextLine(
        title=_(u'Involved Investigator Site URI'),
        description=_(u'Uniform Resource Identifier for the involved investigator site predicate.'),
        required=True,
    )
    bmNameURI = schema.TextLine(
        title=_(u'BM Name URI'),
        description=_(u'Uniform Resource Identifier for the BM name predicate.'),
        required=True,
    )
    coordinateInvestigatorSiteURI = schema.TextLine(
        title=_(u'Coordinating Investigator Site URI'),
        description=_(u'Uniform Resource Identifier for the coordinating site predicate.'),
        required=True,
    )
    leadInvestigatorSiteURI = schema.TextLine(
        title=_(u'Lead Investigator Site URI'),
        description=_(u'Uniform Resource Identifier for the lead investigator site predicate.'),
        required=True,
    )
    collaborativeGroupTextURI = schema.TextLine(
        title=_(u'Collaborative Group Text URI'),
        description=_(u'Uniform Resource Identifier for the collaborative group text predicate.'),
        required=True,
    )
    phasedStatusURI = schema.TextLine(
        title=_(u'Phased Status URI'),
        description=_(u'Uniform Resource Identifier for the phased status predicate.'),
        required=True,
    )
    aimsURI = schema.TextLine(
        title=_(u'Aims URI'),
        description=_(u'Uniform Resource Identifier for the aims predicate.'),
        required=True,
    )
    analyticMethodURI = schema.TextLine(
        title=_(u'Analytic Method URI'),
        description=_(u'Uniform Resource Identifier for the analytic method predicate.'),
        required=True,
    )
    blindingURI = schema.TextLine(
        title=_(u'Blinding URI'),
        description=_(u'Uniform Resource Identifier for the blinding predicate.'),
        required=True,
    )
    cancerTypeURI = schema.TextLine(
        title=_(u'Cancer Type URI'),
        description=_(u'Uniform Resource Identifier for the cancer type predicate.'),
        required=True,
    )
    commentsURI = schema.TextLine(
        title=_(u'Comments URI'),
        description=_(u'Uniform Resource Identifier for the comments predicate.'),
        required=True,
    )
    dataSharingPlanURI = schema.TextLine(
        title=_(u'Data Sharing Plan URI'),
        description=_(u'Uniform Resource Identifier for the data sharing plan predicate.'),
        required=True,
    )
    inSituDataSharingPlanURI = schema.TextLine(
        title=_(u'In-Situ Data Sharing Plan URI'),
        description=_(u'Uniform Resource Identifier for the in-situ data sharing plan predicate.'),
        required=True,
    )
    finishDateURI = schema.TextLine(
        title=_(u'Finish Date URI'),
        description=_(u'Uniform Resource Identifier for the finish date predicate.'),
        required=True,
    )
    estimatedFinishDateURI = schema.TextLine(
        title=_(u'Estimated Finish Date URI'),
        description=_(u'Uniform Resource Identifier for the estimated finish date predicate.'),
        required=True,
    )
    startDateURI = schema.TextLine(
        title=_(u'Start Date URI'),
        description=_(u'Uniform Resource Identifier for the start date predicate.'),
        required=True,
    )
    designURI = schema.TextLine(
        title=_(u'Design URI'),
        description=_(u'Uniform Resource Identifier for the design predicate.'),
        required=True,
    )
    fieldOfResearchURI = schema.TextLine(
        title=_(u'Field of Research URI'),
        description=_(u'Uniform Resource Identifier for the field of research predicate.'),
        required=True,
    )
    abbreviatedNameURI = schema.TextLine(
        title=_(u'Abbreviated Name URI'),
        description=_(u'Uniform Resource Identifier for the abbreviated name predicate.'),
        required=True,
    )
    objectiveURI = schema.TextLine(
        title=_(u'Objective URI'),
        description=_(u'Uniform Resource Identifier for the objective predicate.'),
        required=True,
    )
    projectFlagURI = schema.TextLine(
        title=_(u'Project Flag URI'),
        description=_(u'Uniform Resource Identifier for the project flag predicate.'),
        required=True,
    )
    protocolTypeURI = schema.TextLine(
        title=_(u'Protocol Type URI'),
        description=_(u'Uniform Resource Identifier for the protocol type predicate.'),
        required=True,
    )
    publicationsURI = schema.TextLine(
        title=_(u'Publications URI'),
        description=_(u'Uniform Resource Identifier for the publications predicate.'),
        required=True,
    )
    outcomeURI = schema.TextLine(
        title=_(u'Outcome URI'),
        description=_(u'Uniform Resource Identifier for the outcome predicate.'),
        required=True,
    )
    secureOutcomeURI = schema.TextLine(
        title=_(u'Secure Outcome URI'),
        description=_(u'Uniform Resource Identifier for the secure outcome predicate.'),
        required=True,
    )
    finalSampleSizeURI = schema.TextLine(
        title=_(u'Final Sample Size URI'),
        description=_(u'Uniform Resource Identifier for the final sample size predicate.'),
        required=True,
    )
    plannedSampleSizeURI = schema.TextLine(
        title=_(u'Planend Sample Size URI'),
        description=_(u'Uniform Resource Identifier for the planned sample size predicate.'),
        required=True,
    )
    isAPilotForURI = schema.TextLine(
        title=_(u'Is A Pilot URI'),
        description=_(u'Uniform Resource Identifier for the "is a pilot" predicate.'),
        required=True,
    )
    obtainsDataFromURI = schema.TextLine(
        title=_(u'Obtains Data From URI'),
        description=_(u'Uniform Resource Identifier for the "obtains data from" predicate.'),
        required=True,
    )
    providesDataToURI = schema.TextLine(
        title=_(u'Provides Data To URI'),
        description=_(u'Uniform Resource Identifier for the "provides data to" predicate.'),
        required=True,
    )
    contributesSpecimensURI = schema.TextLine(
        title=_(u'Contributes Sepcimens URI'),
        description=_(u'Uniform Resource Identifier for the "contributes specimens" predicate.'),
        required=True,
    )
    obtainsSpecimensFromURI = schema.TextLine(
        title=_(u'Obtains Specimens From URI'),
        description=_(u'Uniform Resource Identifier for the "obtains specimens from" predicate.'),
        required=True,
    )
    hasOtherRelationshipURI = schema.TextLine(
        title=_(u'Has Other Relationship URI'),
        description=_(u'Uniform Resource Identifier for the "has other relationship" predicate.'),
        required=True,
    )
    animalSubjectTrainingReceivedURI = schema.TextLine(
        title=_(u'Animal Subject Training Received URI'),
        description=_(u'Uniform Resource Identifier for the predicate that indicates if animal subject training as been received.'),
        required=True,
    )
    humanSubjectTrainingReceivedURI = schema.TextLine(
        title=_(u'Human Subject Training Received URI'),
        description=_(u'Uniform Resource Identifier for the predicate that indicates if human subject training as been received.'),
        required=True,
    )
    irbApprovalNeededURI = schema.TextLine(
        title=_(u'IRB Approval Needed URI'),
        description=_(u'Uniform Resource Identifier for the predicate that indicates if IRB approval is still needed.'),
        required=True,
    )
    currentIRBApprovalDateURI = schema.TextLine(
        title=_(u'Current IRB Approval Date URI'),
        description=_(u'Uniform Resource Identifier for the predicate that tells the current IRB approval date.'),
        required=True,
    )
    originalIRBApprovalDateURI = schema.TextLine(
        title=_(u'Original IRB Approval Date URI'),
        description=_(u'Uniform Resource Identifier for the predicate that tells of the original date of IRB approval.'),
        required=True,
    )
    irbExpirationDateURI = schema.TextLine(
        title=_(u'IRB Expiration Date URI'),
        description=_(u'Uniform Resource Identifier for the predicate that tells when the IRB will expire.'),
        required=True,
    )
    generalIRBNotesURI = schema.TextLine(
        title=_(u'General IRB Notes URI'),
        description=_(u'Uniform Resource Identifier for the predicate that lists general notes about the IRB.'),
        required=True,
    )
    irbNumberURI = schema.TextLine(
        title=_(u'IRB Number URI'),
        description=_(u'Uniform Resource Identifier for the predicate that identifies the IRB number.'),
        required=True,
    )
    siteRoleURI = schema.TextLine(
        title=_(u'Site Role URI'),
        description=_(u'Uniform Resource Identifier for the predicate that lists the roles the site participates in.'),
        required=True,
    )
    reportingStageURI = schema.TextLine(
        title=_(u'Report Stage URI'),
        description=_(u'Uniform Resource Identifier for the predicate that names the stages of reporting.'),
        required=True,
    )
    eligibilityCriteriaURI = schema.TextLine(
        title=_(u'Eligibility Criteria URI'),
        description=_(u'Uniform Resource Identifier for the predicate that identifies the eligibility criteria.'),
        required=True,
    )


class _Identified(object):
    def __init__(self, identifier):
        self.identifier = identifier
    def __lt__(self, other):
        return self.identifier < other.identifier
    def __le__(self, other):
        return self.identifier <= other.identifier
    def __eq__(self, other):
        return self.identifier == other.identifier
    def __ne__(self, other):
        return self.identifier != other.identifier
    def __gt__(self, other):
        return self.identifier > other.identifier
    def __ge__(self, other):
        return self.identifier >= other.identifier
    def __repr__(self):
        return '%s(identifier=%s,attributes=%r)' % (self.__class__.__name__, self.identifier, self.attributes)
    def __hash__(self):
        return hash(self.identifier)
    def addToGraph(self, graph, context):
        raise NotImplementedError('Subclasses must implement %s.addToGraph' % self.__class__.__name__)


class _Slotted(_Identified):
    def __init__(self, identifier):
        super(_Slotted, self).__init__(identifier)
        self.slots = {}


class Study(_Slotted):
    def __init__(self, identifier):
        super(Study, self).__init__(identifier)
    def addToGraph(self, graph, context):
        subjectURI = URIRef(context.uriPrefix + self.identifier)
        for slotName, attrName in (
            ('Eligibility_criteria', 'eligibilityCriteriaURI'),
            ('Protocol_Abstract', 'abstractURI'),
            ('Title', 'titleURI')
        ):
            value = self.slots.get(slotName, None)
            if not value: continue
            predicateURI = URIRef(getattr(context, attrName))
            graph.add((subjectURI, predicateURI, Literal(value)))

_specificsPredicates = {
    'animalTraining': 'animalSubjectTrainingReceivedURI',
    'humanTraining': 'humanSubjectTrainingReceivedURI',
    'irbApprovalNeeded': 'irbApprovalNeededURI',
    'irbCurrentApprovalDate': 'currentIRBApprovalDateURI',
    'irbOriginalApprovalDate': 'originalIRBApprovalDateURI',
    'irbExpirationDate': 'irbExpirationDateURI',
    'irbNotes': 'generalIRBNotesURI',
    'irbNumber': 'irbNumberURI',
}

_miscSlots = {
    'BiomarkerName':                        'bmNameURI',
    'Eligibility_criteria':                 'eligibilityCriteriaURI',
    'Protocol_5_Phase_Status':              'phasedStatusURI',
    'Protocol_Aims':                        'aimsURI',
    'Protocol_Analytic_Method':             'analyticMethodURI',
    'Protocol_Blinding':                    'blindingURI',
    'Protocol_Cancer_Type':                 'cancerTypeURI',
    'Protocol_Collaborative_Group':         'collaborativeGroupTextURI',
    'Protocol_Comments':                    'commentsURI',
    'Protocol_Data_Sharing_Plan':           'dataSharingPlanURI',
    'Protocol_Data_Sharing_Plan_In_Place':  'inSituDataSharingPlanURI',
    'Protocol_Date_Finish':                 'finishDateURI',
    'Protocol_Date_Finish_Estimate':        'estimatedFinishDateURI',
    'Protocol_Date_Start':                  'startDateURI',
    'Protocol_Design':                      'designURI',
    'Protocol_Name_Abbrev':                 'abbreviatedNameURI',
    'Protocol_Objective':                   'objectiveURI',
    'Protocol_or_Project_Flag':             'projectFlagURI',
    'Protocol_Results_Outcome':             'outcomeURI',
    'Protocol_Results_Outcome_Secure_Site': 'secureOutcomeURI',
    'Protocol_Type':                        'protocolTypeURI',
    'Sample_Size_Final':                    'finalSampleSizeURI',
    'Sample_Size_Planned':                  'plannedSampleSizeURI',
}

class Protocol(_Slotted):
    def __init__(self, identifier):
        super(Protocol, self).__init__(identifier)
    def getSubjectURI(self, context):
        return URIRef(context.uriPrefix + self.identifier)
    def _addInvolvedInvestigatorSites(self, graph, specifics, context):
        # FIXME:
        # EDRN Portal versions 3.0.0–4.2.0 cannot handle site-specific information.  It turns out the old
        # RDF Server had a bug and never generated them.  This RDF server does indeed generate site-
        # specific information, but that makes the EDRN Portal choke.  Since we can't update the portal
        # at this time, we'll disable generation of site-specific information for now.
        # 
        # for involvedInvestigatorSiteID in self.slots.get(u'Involved_Investigator_Site_ID', u'').split(u', '):
        #     key = (self.identifier, involvedInvestigatorSiteID)
        #     if key not in specifics: continue
        #     specific = specifics[key]
        #     subject = URIRef(context.siteSpecURIPrefix + self.identifier + u'-' + involvedInvestigatorSiteID)
        #     graph.add((subject, rdflib.RDF.type, URIRef(context.siteSpecificTypeURI)))
        #     for fieldName, predicateFieldName in _specificsPredicates.iteritems():
        #         fieldValue = getattr(specific, fieldName, None)
        #         if not fieldValue: continue
        #         predicateURI = URIRef(getattr(context, predicateFieldName))
        #         graph.add((subject, predicateURI, Literal(fieldValue)))
        #     if specific.siteRoles:
        #         predicateURI = URIRef(context.siteRoleURI)
        #         for roleID in specific.siteRoles.split(u', '):
        #             graph.add((subject, predicateURI, Literal(_siteRoles.get(roleID, u'UNKNOWN'))))
        #     if specific.reportingStages:
        #         predicateURI = URIRef(context.reportingStageURI)
        #         for reportingStageID in specific.reportingStages.split(u', '):
        #             graph.add((subject, predicateURI, Literal(_reportingStages.get(reportingStageID, u'UNKNOWN'))))
        pass
    def _addOtherSites(self, graph, context):
        subjectURI = self.getSubjectURI(context)
        for slotName, predicateFieldName in (
            ('Coordinating_Investigator_Site_ID', 'coordinateInvestigatorSiteURI'),
            ('Lead_Investigator_Site_ID', 'leadInvestigatorSiteURI'),
        ):
            siteIDs = self.slots.get(slotName, u'')
            predicateURI = URIRef(getattr(context, predicateFieldName))
            for siteID in siteIDs.split(u', '):
                graph.add((subjectURI, predicateURI, URIRef(context.siteURIPrefix + siteID)))
    def _addPublications(self, graph, context):
        subjectURI, predicateURI = self.getSubjectURI(context), URIRef(context.publicationsURI)
        for pubID in self.slots.get(u'Protocol_Publications', u'').split(u', '):
            pubID = pubID.strip()
            if not pubID: continue
            graph.add((subjectURI, predicateURI, URIRef(context.publicationURIPrefix + pubID)))
    def _addFieldsOfResearch(self, graph, context):
        subjectURI, predicateURI = self.getSubjectURI(context), URIRef(context.fieldOfResearchURI)
        for fieldOfResearchID in self.slots.get(u'Protocol_Field_of_Research', u'').split(u', '):
            graph.add((subjectURI, predicateURI, Literal(_fieldsOfResearch.get(fieldOfResearchID, u'UNKNOWN'))))
    def _addMiscFields(self, graph, context):
        subjectURI = self.getSubjectURI(context)
        for slotName, predicateFieldName in _miscSlots.iteritems():
            obj = self.slots.get(slotName, None)
            if not obj: continue
            predicateURI = URIRef(getattr(context, predicateFieldName))
            graph.add((subjectURI, predicateURI, Literal(obj)))
    def addToGraph(self, graph, specifics, context):
        self._addInvolvedInvestigatorSites(graph, specifics, context)
        self._addOtherSites(graph, context)
        self._addPublications(graph, context)
        self._addFieldsOfResearch(graph, context)
        self._addMiscFields(graph, context)

_specificsMap = {
    'Animal_Subject_Training_Received': 'animalTraining',
    'Human_Subject_Training_Recieved':  'humanTraining',
    'IRB_Approval_Needed':              'irbApprovalNeeded',
    'IRB_Date_Current_Approval_Date':   'irbCurrentApprovalDate',
    'IRB_Date_Original_Approval_Date':  'irbOriginalApprovalDate',
    'IRB_Expiration_Date':              'irbExpirationDate',
    'IRB_General_Notes':                'irbNotes',
    'IRB_Number':                       'irbNumber',
    'Protocol_ID':                      'protocolID',
    'Protocol_Site_Roles':              'siteRoles',
    'Reporting_Stages':                 'reportingStages',
    'Site_ID':                          'siteID',
}

class Specifics(_Identified):
    def __init__(self, row):
        self.identifier, self.attributes = None, {}
        for key, value in parseTokens(row):
            if key == u'Identifier':
                self.identifier = value
            else:
                self.attributes[_specificsMap[key]] = value
    def __getattr__(self, key):
        return self.attributes.get(key, None)

_relationshipsMap = {
    'contributes specimens to': 'contributesSpecimensURI',
    'is a pilot for':           'isAPilotForURI',
    'obtains data from':        'obtainsDataFromURI',
    'obtains specimens from':   'obtainsSpecimensFromURI',
    'Other, specify':           'hasOtherRelationshipURI',
    'provides data to':         'providesDataToURI',
}

class Relationship(_Identified):
    def __init__(self, row):
        self.identifier = None
        for key, value in parseTokens(row):
            if key == u'Identifier':
                self.identifier = value
            elif key == u'Protocol_1_Identifier':
                self.fromID = value
            elif key == u'Protocol_2_Identifier':
                self.toID = value
            elif key == u'Protocol_relationship_type':
                self.relationshipType = value
    def addToGraph(self, graph, context):
        predicateFieldName = _relationshipsMap.get(self.relationshipType, 'hasOtherRelationshipURI')
        predicateURI = URIRef(getattr(context, predicateFieldName))
        subjectURI, objURI = URIRef(context.uriPrefix + self.fromID), URIRef(context.uriPrefix + self.toID)
        graph.add((subjectURI, predicateURI, objURI))


class DMCCProtocolGraphGenerator(grok.Adapter):
    '''A graph generator that produces statements about EDRN's protocols using the DMCC's ludicrous web service.'''
    grok.provides(IGraphGenerator)
    grok.context(IDMCCProtocolRDFGenerator)
    @property
    def verificationNum(self):
        return self.context.verificationNum if self.context.verificationNum else DEFAULT_VERIFICATION_NUM
    @property
    def client(self):
        return get_suds_client(self.context.webServiceURL, self.context)
    def getSlottedItems(self, operation, kind):
        function = getattr(self.client.service, operation)
        horribleString = function(self.verificationNum)
        objects = {}
        obj = None
        for row in splitDMCCRows(horribleString):
            lastSlot = None
            for key, value in parseTokens(row):
                if key == u'Identifier':
                    if obj is None or obj.identifier != value:
                        obj = kind(value)
                        objects[value] = obj
                elif key == u'slot':
                    lastSlot = value
                elif key == u'value':
                    if lastSlot is None:
                        raise ValueError('Value with no preceding slot in row "%r"' % row)
                    obj.slots[lastSlot] = value
                    lastSlot = None
        return objects
    def getStudies(self):
        return self.getSlottedItems(self.context.protocolOrStudyOperation, Study)
    def getProtocols(self):
        return self.getSlottedItems(self.context.edrnProtocolOperation, Protocol)
    def getSpecifics(self):
        function = getattr(self.client.service, self.context.protoSiteSpecificsOperation)
        horribleString = function(self.verificationNum)
        specifics = {}
        for row in splitDMCCRows(horribleString):
            specific = Specifics(row)
            specifics[(specific.protocolID, specific.siteID)] = specific
        return specifics
    def getRelationships(self):
        function = getattr(self.client.service, self.context.protoProtoRelationshipOperation)
        horribleString = function(self.verificationNum)
        relationships = []
        for row in splitDMCCRows(horribleString):
            relationships.append(Relationship(row))
        return relationships
    def generateGraph(self):
        graph = rdflib.Graph()
        # studies, specifics, relationships = self.getStudies(), self.getSpecifics(), self.getRelationships()
        studies = self.getStudies()
        specifics = self.getSpecifics()
        relationships = self.getRelationships()
        protocols = self.getProtocols()
        for study in studies.itervalues():
            subjectURI = URIRef(self.context.uriPrefix + study.identifier)
            graph.add((subjectURI, rdflib.RDF.type, URIRef(self.context.typeURI)))
            study.addToGraph(graph, self.context)
            if study.identifier in protocols:
                protocol = protocols[study.identifier]
                protocol.addToGraph(graph, specifics, self.context)
        for relation in relationships:
            relation.addToGraph(graph, self.context)
        for protocol in protocols.itervalues():
            protocol.addToGraph(graph, specifics, self.context)
        # C'est tout.
        return graph
