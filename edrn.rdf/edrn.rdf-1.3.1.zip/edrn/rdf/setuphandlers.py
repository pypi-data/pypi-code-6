# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from z3c.relationfield import RelationValue
from ZODB.DemoStorage import DemoStorage
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

_dmccURL = u'https://www.compass.fhcrc.org/edrn_ws/ws_newcompass.asmx?WSDL'

def addDCTitle(context, key):
    createContentInContainer(
        context,
        'edrn.rdf.literalpredicatehandler',
        'title',
        title=key,
        description=u'''Maps from DMCC's "Title" key to the Dublin Core title term.''',
        predicateURI=u'http://purl.org/dc/terms/title'
    )

def addDCDescription(context, key):
    createContentInContainer(
        context,
        'edrn.rdf.literalpredicatehandler',
        title=key,
        description=u'''Maps from DMCC's "Description" key to the Dublin Core description term.''',
        predicateURI=u'http://purl.org/dc/terms/description'
    )

def createBodySystemsGenerator(context):
    generator = createContentInContainer(
        context,
        'edrn.rdf.simpledmccrdfgenerator',
        title=u'Body Systems Generator',
        description=u'Generates graphs describing organs and other body systems.',
        webServiceURL=_dmccURL,
        operationName=u'Body_System',
        uriPrefix=u'http://edrn.nci.nih.gov/data/body-systems/',
        identifyingKey=u'Identifier',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#BodySystem'
    )
    addDCTitle(generator, u'item_Title')
    addDCDescription(generator, u'Description')
    return generator

def createDiseaseGenerator(context):
    generator = createContentInContainer(
        context,
        'edrn.rdf.simpledmccrdfgenerator',
        title=u'Diseases Generator',
        description=u'Generates graphs describing diseases that affect body systems.',
        webServiceURL=_dmccURL,
        operationName=u'Disease',
        uriPrefix=u'http://edrn.nci.nih.gov/data/diseases/',
        identifyingKey=u'Identifier',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Disease'
    )
    addDCTitle(generator, u'item_Title')
    addDCDescription(generator, u'description')
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'icd9',
        description=u'''Maps from DMCC's "icd9" key to our EDRN-specific predicate for ICD9 code.''',
        predicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#icd9'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'icd10',
        description=u'''Maps from DMCC's "icd10" key to our EDRN-specific predicate for ICD10 code.''',
        predicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#icd10'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'body_system',
        description=u'''Maps DMCC's "body_system" to a reference to a body system.''',
        predicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#bodySystemsAffected',
        uriPrefix=u'http://edrn.nci.nih.gov/data/body-systems/'
    )
    return generator

def createPublicationGenerator(context):
    generator = createContentInContainer(
        context,
        'edrn.rdf.simpledmccrdfgenerator',
        title=u'Publications Generator',
        description=u'Generates graphs describing articles published by EDRN.',
        webServiceURL=_dmccURL,
        operationName=u'Publication',
        uriPrefix=u'http://edrn.nci.nih.gov/data/pubs/',
        identifyingKey=u'Identifier',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Publication'
    )
    addDCTitle(generator, u'item_Title')
    addDCDescription(generator, u'Description')
    createContentInContainer(
        generator,
        'edrn.rdf.multiliteralpredicatehandler',
        title=u'Author',
        description=u'''Maps from DMCC's "Author" key to zero-or-more Dublin Core "creator" terms.''',
        predicateURI=u'http://purl.org/dc/terms/author'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Issue',
        description=u'''Maps from DMCC's "Issue" key to our EDRN-specific predicate for an issue of a periodical.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#issue'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Journal',
        description=u'''Maps from DMCC's "Journal" key to our EDRN-specific predicate for the title of a periodical.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#journal'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'PMID',
        description=u'''Maps from DMCC's "PMID" key to our EDRN-specific predicate for the PubMed identification of an article.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#pmid'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Publication_URL',
        description=u'''Maps from DMCC's "Publication_URL" key to a URL to the article.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#pubURL',
        uriPrefix=u'',
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Volume',
        description=u'''Maps from DMCC's "Volume" key to our EDRN-specific predicate for the volume number of a periodical.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#volume'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Year',
        description=u'''Maps from DMCC's "Year" key to our EDRN-specific predicate for the publication year of a periodical.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#year'
    )
    return generator

def createSiteGenerator(context):
    generator = createContentInContainer(
        context,
        'edrn.rdf.simpledmccrdfgenerator',
        title=u'Sites Generator',
        description=u'Generates graphs describing the member sites of EDRN.',
        webServiceURL=_dmccURL,
        operationName=u'Site',
        uriPrefix=u'http://edrn.nci.nih.gov/data/sites/',
        identifyingKey=u'Identifier',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Site'
    )
    addDCTitle(generator, u'item_Title')
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Institution_Name_Abbrev',
        description=u'''Maps from DMCC's Institution_Name_Abbrev to EDRN-specific predicate for abbreviated name.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#abbrevName',
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Associate_Members_Sponsor',
        description=u'''Maps from DMCC's Associate_Members_Sponsor to EDRN-specific predicate for sponsoring site.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#sponsor',
        uriPrefix=u'http://edrn.nci.nih.gov/data/sites/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'EDRN_Funding_Date_Start',
        description=u'''Maps from DMCC's EDRN_Funding_Date_Start to EDRN-specific predicate for starting date of funding.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#fundStart',
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'EDRN_Funding_Date_Finish',
        description=u'''Maps from DMCC's EDRN_Funding_Date_Finish to EDRN-specific predicate for ending date of funding.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#fundEnd',
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'FWA_Number',
        description=u'''Maps from DMCC's FWA_Number to EDRN-specific predicate for the so-called "FWA" number. Fwa!''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#fwa',
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'ID_for_Principal_Investigator',
        description=u'''Maps from DMCC's ID_for_Principal_Investigator to EDRN-specific predicate for the PI.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#pi',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'IDs_for_CoPrincipalInvestigators',
        description=u'''Maps from DMCC's IDs_for_CoPrincipalInvestigators to EDRN-specific predicate for co-PIs.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#copi',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'IDs_for_CoInvestigators',
        description=u'''Maps from DMCC's IDs_for_CoInvestigators to EDRN-specific predicate for co-investigators.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#coi',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'IDs_for_Investigators',
        description=u'''Maps from DMCC's IDs_for_Investigators to EDRN-specific predicate for investigators.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#investigator',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'IDs_for_Staff',
        description=u'''Maps from DMCC's IDs_for_Staff to EDRN-specific predicate for peons.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#staff',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Site_Program_Description',
        description=u'''Maps from DMCC's Site_Program_Description to EDRN-specific predicate for the site's program.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#program'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Institution_URL',
        description=u'''Maps from DMCC's Institution_URL to EDRN-specific predicate for the site's home page.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#url',
        uriPrefix=u''
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Member_Type',
        description=u'''Maps from DMCC's Member_Type to EDRN-specific predicate for the kind of site.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#memberType'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Member_Type_Historical_Notes',
        description=u'''Maps from DMCC's Member_Type_Historical_Notes to EDRN-specific predicate for various notes.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#historicalNotes'
    )
    return generator

def createPersonGenerator(context):
    generator = createContentInContainer(
        context,
        'edrn.rdf.simpledmccrdfgenerator',
        title=u'Person Generator',
        description=u'Generates graphs describing the people of EDRN.',
        webServiceURL=_dmccURL,
        operationName=u'Registered_Person',
        uriPrefix=u'http://edrn.nci.nih.gov/data/registered-person/',
        identifyingKey=u'Identifier',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Person'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Name_First',
        description=u'''Maps from DMCC's Name_First to the FOAF predicate for given name.''',
        predicateURI=u'http://xmlns.com/foaf/0.1/givenname'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Name_Middle',
        description=u'''Maps from DMCC's Name_Middle to EDRN-specific predicate for middle name.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#middleName'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Name_Last',
        description=u'''Maps from DMCC's Name_Last to the FOAF predicate for surname.''',
        predicateURI=u'http://xmlns.com/foaf/0.1/surname'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Phone',
        description=u'''Maps from DMCC's Phone to the FOAF predicate for phone.''',
        predicateURI=u'http://xmlns.com/foaf/0.1/phone'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Email',
        description=u'''Maps from DMCC's Email to the FOAF predicate for "mbox".''',
        predicateURI=u'http://xmlns.com/foaf/0.1/mbox',
        uriPrefix=u'mailto:'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Fax',
        description=u'''Maps from DMCC's Fax to the VCARD predicate for "fax".''',
        predicateURI=u'http://www.w3.org/2001/vcard-rdf/3.0#fax'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Speciality',
        description=u'''Maps from DMCC's Speciality to EDRN-specific predicate for speciality.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#speciality'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Photo_file_name',
        description=u'''Maps from DMCC's Photo_file_name to the FOAF predicate for photograph.''',
        predicateURI=u'http://xmlns.com/foaf/0.1/img',
        uriPrefix=u'http://edrn.jpl.nasa.gov/dmcc/staff-photographs/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'EDRN_Title',
        description=u'''Maps from DMCC's EDRN_Title to EDRN-specific predicate for EDRN job title.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#EDRN_Title'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'userID',
        description=u'''Maps from DMCC's userID to the FOAF predicate for account name.''',
        predicateURI=u'http://xmlns.com/foaf/0.1/accountName'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.referencepredicatehandler',
        title=u'Site_id',
        description=u'''Maps from DMCC's Site_id to EDRN-specific predicate for the member's site.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#site',
        uriPrefix=u'http://edrn.nci.nih.gov/data/sites/'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_Address1',
        description=u'''Maps from DMCC's Mailing_Address1 to EDRN-specific predicate for line 1 of mailing address.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#addr1'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_Address2',
        description=u'''Maps from DMCC's Mailing_Address2 to EDRN-specific predicate for line 2 of mailing address.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#addr2'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_City',
        description=u'''Maps from DMCC's Mailing_City to EDRN-specific predicate for mailing city.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#city'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_State',
        description=u'''Maps from DMCC's Mailing_State to EDRN-specific predicate for mailing state.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#state'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_Zip',
        description=u'''Maps from DMCC's Mailing_Zip to EDRN-specific predicate for postal code.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#postalCode'
    )
    createContentInContainer(
        generator,
        'edrn.rdf.literalpredicatehandler',
        title=u'Mailing_Country',
        description=u'''Maps from DMCC's Mailing_Country to EDRN-specific predicate for mailing country.''',
        predicateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#country'
    )
    return generator

def createCommitteeGenerator(context):
    return createContentInContainer(
        context,
        'edrn.rdf.dmcccommitteerdfgenerator',
        title=u'Committees Generator',
        description=u'Generates graphs describing the EDRN\'s committees.',
        webServiceURL=_dmccURL,
        committeeOperation=u'Committees',
        membershipOperation=u'Committee_Membership',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Committee',
        uriPrefix=u'http://edrn.nci.nih.gov/data/committees/',
        personPrefix=u'http://edrn.nci.nih.gov/data/registered-person/',
        titlePredicateURI=u'http://purl.org/dc/terms/title',
        abbrevNamePredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#abbreviatedName',
        committeeTypePredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#committeeType',
        chairPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#chair',
        coChairPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#coChair',
        consultantPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#consultant',
        memberPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#member'
    )

def createProtocolGenerator(context):
    return createContentInContainer(
        context,
        'edrn.rdf.dmccprotocolrdfgenerator',
        title=u'Protocols Generator',
        description=u'Generates graphs describing EDRN protocols and studies.',
        webServiceURL=_dmccURL,
        protocolOrStudyOperation=u'Protocol_or_Study',
        edrnProtocolOperation=u'EDRN_Protocol',
        protoSiteSpecificsOperation=u'Protocol_Site_Specifics',
        protoProtoRelationshipOperation=u'Protocol_Protocol_Relationship',
        typeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#Protocol',
        siteSpecificTypeURI=u'http://edrn.nci.nih.gov/rdf/types.rdf#ProtocolSiteSpecific',
        uriPrefix=u'http://edrn.nci.nih.gov/data/protocols/',
        siteSpecURIPrefix=u'http://edrn.nci.nih.gov/data/protocols/site-specific/',
        publicationURIPrefix=u'http://edrn.nci.nih.gov/data/pubs/',
        siteURIPrefix=u'http://edrn.nci.nih.gov/data/sites/',
        titleURI=u'http://purl.org/dc/terms/title',
        abstractURI=u'http://purl.org/dc/terms/description',
        involvedInvestigatorSiteURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#involvedInvestigatorSite',
        bmNameURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#bmName',
        coordinateInvestigatorSiteURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#coordinatingInvestigatorSite',
        leadInvestigatorSiteURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#leadInvestigatorSite',
        collaborativeGroupTextURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#collaborativeGroupText',
        phasedStatusURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#phasedStatus',
        aimsURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#aims',
        analyticMethodURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#analyticMethod',
        blindingURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#blinding',
        cancerTypeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#cancerType',
        commentsURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#comments',
        dataSharingPlanURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#dataSharingPlan',
        inSituDataSharingPlanURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#inSituDataSharingPlan',
        finishDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#finishDate',
        estimatedFinishDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#estimatedFinishDate',
        startDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#startDate',
        designURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#design',
        fieldOfResearchURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#fieldOfResearch',
        abbreviatedNameURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
        objectiveURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#objective',
        projectFlagURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#projectFlag',
        protocolTypeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#protocolType',
        publicationsURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#publications',
        outcomeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#outcome',
        secureOutcomeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#secureOutcome',
        finalSampleSizeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#finalSampleSize',
        plannedSampleSizeURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#plannedSampleSize',
        isAPilotForURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#isAPilot',
        obtainsDataFromURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#obtainsDataFrom',
        providesDataToURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#providesDataTo',
        contributesSpecimensURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#contributesSpecimensTo',
        obtainsSpecimensFromURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#obtainsSpecimensFrom',
        hasOtherRelationshipURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#hasOtherRelationship',
        animalSubjectTrainingReceivedURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#animalSubjectTrainingReceived',
        humanSubjectTrainingReceivedURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#humanSubjectTrainingReceived',
        irbApprovalNeededURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#irbApprovalNeeded',
        currentIRBApprovalDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#currentIRBApprovalDate',
        originalIRBApprovalDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#originalIRBApprovalDate',
        irbExpirationDateURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#irbExpirationDate',
        generalIRBNotesURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#irbNotes',
        irbNumberURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#irbNumber',
        siteRoleURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#siteRole',
        reportingStageURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#reportingStage',
        eligibilityCriteriaURI=u'http://edrn.nci.nih.gov/rdf/schema.rdf#eligibilityCriteria'
    )

def createRDFGenerators(context):
    generators = {}
    folder = context[context.invokeFactory(
        'Folder', 'rdf-generators', title=u'RDF Generators', description=u'These objects are used to generate graphs of statements.'
    )]
    generators['body-systems']      = createBodySystemsGenerator(folder)
    generators['committees']        = createCommitteeGenerator(folder)
    generators['diseases']          = createDiseaseGenerator(folder)
    generators['protocols']         = createProtocolGenerator(folder)
    generators['publications']      = createPublicationGenerator(folder)
    generators['registered-person'] = createPersonGenerator(folder)
    generators['sites']             = createSiteGenerator(folder)
    return generators

def createRDFSources(context, generators):
    folder = context[context.invokeFactory(
        'Folder', 'rdf-data', title=u'RDF Sources', description=u'Sources of RDF information for EDRN.'
    )]
    for objID, title, desc in (
        ('body-systems', u'Body Systems', u'Source of RDF for body systems.'),
        ('diseases', u'Diseases', u'Source of RDF for diseases.'),
        ('publications', u'Publications', u'Source of RDF for publications.'),
        ('sites', u'Sites', u'Source of RDF for EDRN\'s member sites.'),
        ('registered-person', u'Registered Person', u'Source of RDF for EDRN\'s people.'),
        ('committees', u'Committees', u'Source of RDF for committees and working groups in EDRN.'),
        ('protocols', u'Protocols', u'Source of RDF for EDRN\'s various protocols and studies.')
    ):
        generator = RelationValue(generators[objID])
        createContentInContainer(folder, 'edrn.rdf.rdfsource', title=title, description=desc, generator=generator, active=True)
    
def publish(item, wfTool):
    try:
        wfTool.doActionFor(item, action='publish')
        item.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(item):
        for itemID, subItem in item.contentItems():
            publish(subItem, wfTool)

def installInitialSources(portal):
    # Don't bother if we're running under test fixture
    if hasattr(portal._p_jar, 'db') and isinstance(portal._p_jar.db().storage, DemoStorage): return
    if 'rdf-generators' in portal.keys():
        portal.manage_delObjects('rdf-generators')
    if 'rdf-data' in portal.keys():
        portal.manage_delObjects('rdf-data')
    generators = createRDFGenerators(portal)
    wfTool = getToolByName(portal, 'portal_workflow')
    publish(portal['rdf-generators'], wfTool)
    intIDs = getUtility(IIntIds)
    for key, generator in generators.items():
        intID = intIDs.getId(generator)
        generators[key] = intID
    createRDFSources(portal, generators)
    publish(portal['rdf-data'], wfTool)

def setupVarious(context):
    if context.readDataFile('edrn.rdf.marker.txt') is None: return
    portal = context.getSite()
    installInitialSources(portal)
