import rdflib
from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF
import datetime

class Entity:
    def __init__(self, entity_uri, title, created, creator, description=None,
                 rights=None, confidentialityStatus=None, metadataUri=None, downloadURL=None):
        """
        Creates objects of type PROMS-O Entity

        :param entity_uri: A URI for this Entity. Must be either a URI or a URIRef(BNode()) or None. If None, a BNode will be created for the Entity.
        :param title: dc:title
        :param description: dc:description
        :param created: dc:created
        :param creator: dc:creator
        :param rights: dc:rights
        :param confidentialityStatus: The confidentiality status of this Entity
        :param metadataUri: A URI leading to this Entity's metadata document (expected to be a document conformant to a schema such as ANZLIC or ISO19115)
        :param downloadURL: A URL leading to this Entity's data
        :return: nothing (an Entity object is created)
        """

        #region Set instance variables
        if entity_uri is None:
            self.entity_uri = BNode()
        else:
            #it is a URIRef or a BNode elsewhere specified
            self.entity_uri = entity_uri

        if type(self.entity_uri) == rdflib.BNode:
            self.title = title
            self.created = created
            self.creator = creator
            if description:
                self.description = description
            if rights:
                self.license = rights
            else:
                self.license = None                
            if confidentialityStatus:
                self.confidentialityStatus = confidentialityStatus
            else:
                self.confidentialityStatus = None                  
            if metadataUri:
                self.metadataUri = metadataUri
            else:
                self.metadataUri = None
            if downloadURL:
                self.downloadURL = downloadURL
            else:
                self.downloadURL = None
        #endregion Set instance variables

        #region Add instance variables to graph
        self.g = Graph()

        PROV = Namespace('http://www.w3.org/ns/prov#')

        self.g.add((URIRef(self.entity_uri),
                    RDF.type,
                    PROV.Entity))

        if type(self.entity_uri) == rdflib.BNode:
            XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
            PROMS = Namespace('http://promsns.org/def/proms#')
            DC = Namespace('http://purl.org/dc/elements/1.1/')
            DCAT = Namespace('http://www.w3.org/ns/dcat#')

            self.g.add((URIRef(self.entity_uri),
                        DC.title,
                        Literal(self.title, datatype=XSD.string)))

            if isinstance(self.created, datetime.datetime):
                self.g.add((URIRef(self.entity_uri),
                            DC.created,
                            Literal(self.created.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
            else:
                if isinstance(self.created, int):
                   self.g.add((URIRef(self.entity_uri),
                               PROMS.createdAtTimeDiffStep,
                               Literal(self.created, datatype=XSD.integer)))

            self.g.add((URIRef(self.entity_uri),
                        DC.creator,
                        Literal(self.creator, datatype=XSD.string)))

            if self.description:
                self.g.add((URIRef(self.entity_uri),
                            DC.description,
                            Literal(self.description, datatype=XSD.string)))

            if self.license:
                self.g.add((URIRef(self.entity_uri),
                            DC.license,
                            URIRef(self.license)))

            if self.confidentialityStatus:
                self.g.add((URIRef(self.entity_uri),
                            PROMS.confidentialityStatus,
                            URIRef(self.confidentialityStatus)))

            if self.metadataUri:
                self.g.add((URIRef(self.entity_uri),
                            PROMS.metadataUri,
                            Literal(self.metadataUri, datatype=XSD.anyUri)))

            if self.downloadURL:
                self.g.add((URIRef(self.entity_uri),
                            DCAT.downloadURL,
                            Literal(self.downloadURL, datatype=XSD.anyUri)))
        #endregion

        return

    def get_id(self):
        """
        Get the node URI of this Entity, whether a BNode or URI.

        :return: Either a BNode or a URI
        """
        return URIRef(self.entity_uri)

    def get_graph(self):
        """
        Generates the RDF graph of this Entity

        :return: This Entity's RDF graph according to PROMS-O
        """
        return self.g


class ConfidentialityStatus:
    """
    This class specifies acceptable URI values for
    the proms:confidentialityStatus property of PROMS-O Entities.
    """
    PublicDomain = 'http://promsns.org/def/proms/confidentiality/publicdomain'
    Private = 'http://promsns.org/def/proms/confidentiality/private'
    AccessAvailableOnRequest = 'http://promsns.org/def/proms/confidentiality/accessavailableonrequest'
    OwnerDepartmentOnly = 'http://promsns.org/def/proms/confidentiality/ownerdepartmentonly'
    IndigenousSensitive = 'http://promsns.org/def/proms/confidentiality/indigenoussensitive'