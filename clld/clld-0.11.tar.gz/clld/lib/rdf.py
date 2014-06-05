"""
This module provides functionality for handling our data as rdf.
"""
from collections import namedtuple
from cStringIO import StringIO

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import (
    Namespace, DC, DCTERMS, DOAP, FOAF, OWL, RDF, RDFS, SKOS, VOID, XMLNS, XSD,
)
# make flake8 happy, but still have the following importable from here:
assert DOAP
assert XMLNS

from clld.util import encoded


Notation = namedtuple('Notation', 'name extension mimetype uri')

FORMATS = dict((n.name, n) for n in [
    Notation('xml', 'rdf', 'application/rdf+xml', 'http://www.w3.org/ns/formats/RDF_XML'),
    Notation('n3', 'n3', 'text/n3', 'http://www.w3.org/ns/formats/N3'),
    Notation('nt', 'nt', 'text/nt', 'http://www.w3.org/ns/formats/N-Triples'),
    Notation('turtle', 'ttl', 'text/turtle', 'http://www.w3.org/ns/formats/Turtle')])

NAMESPACES = {
    "rdf": RDF,
    "void": VOID,
    "foaf": FOAF,
    "frbr": Namespace("http://purl.org/vocab/frbr/core#"),
    "dcterms": DCTERMS,
    "rdfs": RDFS,
    "geo": Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
    "isbd": Namespace("http://iflastandards.info/ns/isbd/elements/"),
    "skos": SKOS,
    "dc": DC,
    "gold": Namespace("http://purl.org/linguistics/gold/"),
    "lexvo": Namespace("http://lexvo.org/ontology#"),
    "vcard": Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"),
    "bibo": Namespace("http://purl.org/ontology/bibo/"),
    "owl": OWL,
    "xsd": XSD,
}


def expand_prefix(p):
    """
    >>> assert expand_prefix('noprefix:lname') == 'noprefix:lname'
    >>> assert expand_prefix('rdf:nolname') == 'rdf:nolname'
    >>> assert expand_prefix('nocolon') == 'nocolon'

    :param p: a qualified name in prefix:localname notation or a URL.
    :return: a string URL or a URIRef
    """
    if isinstance(p, basestring) and ':' in p:
        prefix, name = p.split(':', 1)
        if prefix in NAMESPACES:
            try:
                return getattr(NAMESPACES[prefix], name)
            except Exception:
                pass
    return p


def url_for_qname(qname):
    """
    >>> assert url_for_qname('dcterms:title') == 'http://purl.org/dc/terms/title'
    """
    return str(expand_prefix(qname))


class ClldGraph(Graph):
    """augment the standard rdflib.Graph by making sure our standard ns prefixes are
    always bound.
    """
    def __init__(self, *args, **kw):
        super(ClldGraph, self).__init__(*args, **kw)
        for prefix, ns in NAMESPACES.items():
            self.bind(prefix, ns)


def properties_as_xml_snippet(subject, props):
    """somewhat ugly way to get at a snippet of an rdf-xml serialization of properties
    of a subject.

    >>> p = properties_as_xml_snippet('http://example.org', [('dcterms:title', 'ttt')])
    >>> assert 'ttt' in p
    """
    if isinstance(subject, basestring):
        subject = URIRef(subject)
    g = ClldGraph()
    if props:
        for p, o in props:
            p = expand_prefix(p)
            if isinstance(o, basestring):
                if o.startswith('http://') or o.startswith('https://'):
                    o = URIRef(o)
                else:
                    o = Literal(o)
            g.add((subject, p, o))
    res = []
    in_desc = False
    for line in g.serialize(format='xml').split('\n'):
        if line.strip().startswith('</rdf:Description'):
            break
        if in_desc:
            res.append(line)
        if line.strip().startswith('<rdf:Description'):
            in_desc = True
    return '\n'.join(res).decode('utf8')


def convert(string, from_, to_):
    if from_ == to_:
        return encoded(string)
    assert from_ in FORMATS and to_ in FORMATS
    g = Graph()
    g.parse(StringIO(encoded(string)), format=from_)
    out = StringIO()
    g.serialize(out, format=to_)
    out.seek(0)
    return out.read()
