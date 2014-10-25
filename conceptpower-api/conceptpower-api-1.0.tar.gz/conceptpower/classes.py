import requests
import xml.etree.ElementTree as ET

class Conceptpower:
    """
    Provides simple access to the `Conceptpower
    <http://conceptpower.sourceforge.net/>`_ API.
    
    Set :prop:`.endpoint` and :prop:`.namespace` when subclassing 
    :class:`.Conceptpower` or by passing them as ``kwargs`` to the constructor.
    
    Parameters
    ----------
    kwargs : kwargs
        Set :prop:`.endpoint` and :prop:`.namespace` by passing ``endpoint``
        and ``namespace`` kwargs, respectively. This will have no effect if
        those properties are set in the class definition (e.g. when subclassing
        :class:`.Conceptpower`\.
    """

    # Default behavior is to leave these to the constructor.
    endpoint = None
    namespace = None
    
    def __init__(self, **kwargs):
        # Give first priority to the class definition, if endpoint or namespace
        #  are defined (and not None).
        if self.endpoint is None:
            self.endpoint = kwargs.get(
                "endpoint", "http://chps.asu.edu/conceptpower/rest/")
        
        if self.namespace is None:
            self.namespace = kwargs.get(
               "namespace", "{http://www.digitalhps.org/}")
    
    def search (self, query, pos='Noun'):
        """
        Search for a concept by lemma.
        
        Parameters
        ----------
        query : str
            Search term.
        pos : str
            (default: 'Noun') Part of speach: Noun, Verb, etc.
            
        Returns
        -------
        results : list
        
        Example
        -------
        >>> pprint (cp.search("Bradshaw"))
        [{'conceptList': 'Persons',
          'description': 'Plant ecologist',
          'id': 'http://www.digitalhps.org/concepts/066efc74-8710-4a1f-9111-3a27d880438e',
          'lemma': 'Anthony David Bradshaw (1926-2008)',
          'pos': 'noun',
          'type': 'E21 Person'},
         {'conceptList': 'Persons',
          'description': 'Botanist at the University of Exeter',
          'id': 'http://www.digitalhps.org/concepts/CONe5b55803-1ef6-4abe-b81c-1493e97421df',
          'lemma': 'Margaret E. Bradshaw',
          'pos': 'noun',
          'type': 'E21 Person'},
         {'conceptList': 'Publications',
          'description': 'Bradshaw, Anthony David. 1965. "The evolutionary significance of phenotypic plasticity in plants." Advances in Genetics 13: 115-155.',
          'id': 'http://www.digitalhps.org/concepts/CON76832db2-7abb-4c77-b08e-239017b6a585',
          'lemma': 'Bradshaw 1965',
          'pos': 'noun',
          'type': 'E28 Conceptual Object '},
         {'conceptList': 'Phenotypic Plasticity',
          'description': None,
          'id': 'http://www.digitalhps.org/concepts/72ec32b4-2a20-4d26-ab8f-a173f067542d',
          'lemma': 'Anthony D. Bradshaw',
          'pos': 'noun',
          'type': None}]
        """
        
        url = "{0}ConceptLookup/{1}/{2}".format(self.endpoint, query, pos)
        root = ET.fromstring(requests.get(url).content)
        conceptEntries = root.findall("{0}conceptEntry".format(self.namespace))
        results = [{ node.tag.replace(self.namespace, ''): node.text
                        for node in conceptEntry }
                            for conceptEntry in conceptEntries ]
        return results

    def get (self, uri):
        """
        Retrieve information (by ID or URI) about a concept.
        
        Parameters
        ----------
        uri : str
            The full Conceptpower URI, or an ID, as string. For example: 
            http://www.digitalhps.org/CON7971a85a-49e1-424d-84e6-697262bd2510
            
        Returns
        -------
        data : dict
        
        Example
        -------
        >>> pprint (cp.get("http://www.digitalhps.org/concepts/CON536b243d-3c71-4a5c-ab79-3c7f12765b3f"))
        {'conceptList': 'Persons',
         'description': 'A professor at the Cambridge Botany School',
         'id': 'http://www.digitalhps.org/concepts/CON536b243d-3c71-4a5c-ab79-3c7f12765b3f',
         'lemma': 'Sir Harry Godwin',
         'pos': 'noun',
         'type': 'E21 Person',
         'type_id': '986a7cc9-c0c1-4720-b344-853f08c136ab',
         'type_uri': 'http://www.digitalhps.org/types/TYPE_986a7cc9-c0c1-4720-b344-853f08c136ab'}
        """

        url = "{0}Concept?id={1}".format(self.endpoint, uri)
        root = ET.fromstring(requests.get(url).content)
        conceptEntry = root.findall("{0}conceptEntry".format(self.namespace))[0]
        data = {}

        for snode in conceptEntry:
            data[snode.tag.replace(self.namespace, '')] = snode.text
            if snode.tag == '{0}type'.format(self.namespace):
                data['type_id'] = snode.get('type_id')
                data['type_uri'] = snode.get('type_uri')
        return data