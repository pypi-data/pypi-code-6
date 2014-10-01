from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF
import datetime


class Activity:
    def __init__(self, activity_uri, title, wasAttributedTo, startedAtTime, endedAtTime,
                 description=None, used_entities=None, generated_entities=None, wasInformedBy=None):
        """
        Creates objects of type PROMS-O Activity

        :param activity_uri: A URI for this Activity. Must be either a URI or a None. If None, a BNode will be created for the Activity.
        :param title: dc:title
        :param description: dc:description
        :param wasAttributedTo: prov:wasAttributedTo
        :param startedAtTime: prov:startedAtTime or proms:startedAtTimeDiffStep
        :param endedAtTime: prov:endedAtTime or proms:endedAtTimeDiffStep
        :param wasInformedBy: prov:wasInformedBy
        :param used_entities: List of prov:Entities
        :param generated_entities: List of prov:Entities
        :return: nothing (an initialised Activity object)
        """

        #region Set instance variables
        if activity_uri:
            self.activity_uri = activity_uri
        else:
            self.activity_uri = BNode()

        self.title = title
        self.wasAttributedTo = wasAttributedTo
        self.startedAtTime = startedAtTime
        self.endedAtTime = endedAtTime

        if description:
            self.description = description
        else:
            self.description = None

        if used_entities:
            self.used_entities = used_entities
        else:
            self.used_entities = None

        if generated_entities:
            self.generated_entities = generated_entities
        else:
            self.generated_entities = None

        if wasInformedBy:
            self.wasInformedBy = wasInformedBy
        else:
            self.wasInformedBy = None
        #endregion

        #region Add instance variables to graph
        self.g = Graph()

        PROV = Namespace('http://www.w3.org/ns/prov#')
        PROMS = Namespace('http://promsns.org/def/proms#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        DC = Namespace('http://purl.org/dc/elements/1.1/')

        self.g.add((URIRef(self.activity_uri),
                    RDF.type,
                    PROV.Activity))

        self.g.add((URIRef(self.activity_uri),
                    DC.title,
                    Literal(self.title)))

        self.g.add((URIRef(self.activity_uri),
                    PROV.wasAttributedTo,
                    URIRef(self.wasAttributedTo)))

        if isinstance(self.startedAtTime, datetime.datetime):
            #add an absolute time
            self.g.add((URIRef(self.activity_uri),
                        PROV.startedAtTime,
                        Literal(self.startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
            #add a relative timestep integer
            self.g.add((URIRef(self.activity_uri),
                        PROMS.startedAtTimeDiffStep,
                        Literal(self.startedAtTime, datatype=XSD.integer)))

        if isinstance(self.endedAtTime, datetime.datetime):
            #add an absolute timestep integer
            self.g.add((URIRef(self.activity_uri),
                        PROV.endedAtTime,
                        Literal(self.endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
            #add a relative time
            self.g.add((URIRef(self.activity_uri),
                        PROMS.endedAtTimeDiffStep,
                        Literal(self.endedAtTime, datatype=XSD.integer)))

        if self.description:
            self.g.add((URIRef(self.activity_uri),
                        DC.description,
                        Literal(self.description)))

        if self.used_entities:
            for used_entity in self.used_entities:
                #add the Entity to the graph
                self.g = self.g + used_entity.get_graph()
                #associate the Entity with the Activity
                self.g.add((URIRef(self.activity_uri),
                            PROV.used,
                            URIRef(used_entity.get_id())))

        if self.generated_entities:
            for generated_entity in self.generated_entities:
                #add the Entity to the graph
                self.g = self.g + generated_entity.get_graph()
                #associate the Entity with the Activity
                self.g.add((URIRef(self.activity_uri),
                            PROV.generated,
                            URIRef(generated_entity.get_id())))

        if self.wasInformedBy:
            self.g.add((URIRef(self.activity_uri),
                        PROV.wasInformedBy,
                        URIRef(self.wasInformedBy)))
        #endregion

        return

    def get_id(self):
        """
        Get the node URI of this Activity, whether a BNode or URI.

        :return: Either a BNode or a URI
        """
        return URIRef(self.activity_uri)

    def get_graph(self):
        """
        Generates the RDF graph of this Activity

        :return: This Activity's RDF graph according to PROMS-O
        """
        return self.g



