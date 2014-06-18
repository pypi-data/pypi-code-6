__author__ = 'matt'

import unittest
import json
import logging
import pprint
from rdflib import URIRef, Literal, Graph, XSD

from rdfdict import RDFdict
import rdfdict

logger = logging.getLogger()
pprint = pprint.PrettyPrinter()
pf = pprint.pformat

prefix = 'http://mattclark.net/rdfdict/test#'
s = URIRef(prefix+'s')
p = URIRef(prefix+'p')
o = URIRef(prefix+'o')

lit_float = Literal('1.5', datatype=XSD.float)
lit_int = Literal('1', datatype=XSD.int)
lit_str = Literal('astr', datatype=XSD.string)


test_triples = ((s, p, o),
                (s, p, lit_float),
                (s, p, lit_int),
                (s, p, lit_str))

triplegraph = { s: { p: [o, lit_float, lit_int, lit_str] }}

test_triple_json = '''{ "http://mattclark.net/rdfdict/test#s": { "http://mattclark.net/rdfdict/test#p":
                                        [ "http://mattclark.net/rdfdict/test#o", 1.5, 1, "astr" ]} }'''

class TestRDFdictWithRDFlib(unittest.TestCase):
    def test_literal_converter_is_set(self):
        rd = RDFdict()
        logger.debug(rd.__dict__)
        self.assertEqual(rd._value_converter, rdfdict.json_literal_converter)

    def test_literals_converted(self):
        rd = RDFdict(triples=test_triples)
        json_repr = json.dumps(rd.default_graph())
        self.assertTrue(compare_dicts(json.loads(json_repr), json.loads(test_triple_json)))


def compare_dicts(d1, d2):
    logger.debug('Comparing DICTs:\n%s\n%s' % (pf(d1), pf(d2)))
    if set(d1.keys()) != set(d2.keys()):
        raise ValueError('Dictionary keys do not match:\n%s\n%s' % (pf(d1), pf(d2)))
    for k in d1.keys():
        v1 = d1[k]
        v2 = d2[k]
        logger.debug('Comparing: VALUEs\n%s\n%s' % (pf(v1), pf(v2)))
        if isinstance(v1, dict):
            if not isinstance(v2, dict):
                raise TypeError('Value types do not match: %s, %s' % (type(v1), type(v2)))
            return compare_dicts(v1, v2)
        elif isinstance(v1, list):
            if set(v1) != set(v2):
                raise ValueError('Lists do not match:\n%s\n%s' % (set(v1), set(v2)))
        else:
            if v1 != v2:
                raise ValueError('Values do not match:\n%s\n%s' % (pf(v1), pf(v2)))
    return True