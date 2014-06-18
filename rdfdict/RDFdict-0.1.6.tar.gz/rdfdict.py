__author__ = 'Matt Clark'

try:
    from rdflib import Literal, XSD
    # type conversion based on lists at http://simplejson.readthedocs.org/en/latest/#encoders-and-decoders
    # and at http://www.w3.org/TR/xmlschema-2/#built-in-datatypes
    literal_type_converters = {
        XSD.boolean: bool,
        XSD.byte: int,
        XSD.decimal: long,
        XSD.double: long,
        XSD.float: float,
        XSD.int: int,
        XSD.integer: int,
        XSD.long: long,
        XSD.negativeInteger: int,
        XSD.nonNegativeInteger: long,
        XSD.nonPositiveInteger: long,
        XSD.positiveInteger: int,
        XSD.short: int,
        XSD.unsignedByte: int,
        XSD.unsignedInt: int,
        XSD.unsignedLong: long,
        XSD.unsignedShort: int
    }

    def json_literal_converter(value):
        if not isinstance(value, Literal):
            return value
        elif value.datatype in literal_type_converters:
            return literal_type_converters[value.datatype](value)
        else:
            return str(value)

    default_value_converter = json_literal_converter
except ImportError:
    default_value_converter = lambda x: x



class RDFdict(object):
    def __init__(self, triples=(), quads=(), default_graph='DEFAULT', value_converter=default_value_converter):
        self._maindict = dict()
        self._default_graph_name = default_graph
        self._maindict[default_graph] = dict()
        self._value_converter = value_converter
        for (s, p, o) in triples:
            self.add_triple(s, p, o)
        for (s, p, o, g) in quads:
            self.add_quad(s, p, o, g)

    def graph_names(self):
        return self._maindict.keys()

    def default_graph_name(self):
        return self._default_graph_name

    def graphs(self):
        return self._maindict.iteritems()

    def graph(self, graphname):
        return self._maindict[graphname]

    def default_graph(self):
        return self.graph(self._default_graph_name)

    def add_triple(self, s, p, o):
        self.add_quad(s, p, o, self._default_graph_name)

    def add_quad(self, s, p, o, g):
        if not g:
            g = self._default_graph_name
        graphdict = self._maindict.setdefault(g, dict())
        self._add_triple_to_graph_dict(graphdict, s, p, o)

    def _add_triple_to_graph_dict(self, graphdict, s, p, o):
        o = self._value_converter(o)
        subjectdict = graphdict.setdefault(s, dict())
        if p in subjectdict:
            try:
                subjectdict[p].append(o)
            except AttributeError:
                subjectdict[p] = list((subjectdict[p], o))
        else:
            subjectdict[p] = o

    def __str__(self):
        return self._maindict.__str__()





