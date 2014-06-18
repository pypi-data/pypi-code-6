__author__ = 'matt'

import unittest
import json
import logging
import pprint

from rdfdict import RDFdict

logger = logging.getLogger()
pprint = pprint.PrettyPrinter()
pf = pprint.pformat

quads = (
    ("subject1", "predicate1", "singleobject1", "graph1"),
    ("subject1", "predicate2", "multiobject1", "graph1"),
    ("subject1", "predicate2", "multiobject2", "graph1"),
    ("subject2", "predicate3", "singleobject2", "graph1"),
    ("subject2", "predicate4", "multiobject3", "graph1"),
    ("subject2", "predicate4", "multiobject4", "graph1"),
    ("subject3", "predicate5", "singleobject3", "graph2"),
    ("subject3", "predicate6", "multiobject5", "graph2"),
    ("subject3", "predicate6", "multiobject6", "graph2"),
    ("subject4", "predicate7", "singleobject4", "graph2"),
    ("subject4", "predicate8", "multiobject7", "graph2"),
    ("subject4", "predicate8", "multiobject8", "graph2"),
    ("subject5", "predicate9", "singleobject5", None)
)

quadgraphs = { 'graph1':
            ''' {
                    "subject1": {
                        "predicate1": "singleobject1",
                        "predicate2": [ "multiobject1", "multiobject2" ]
                    },
                    "subject2": {
                        "predicate3": "singleobject2",
                        "predicate4": [ "multiobject3", "multiobject4" ]
                    }
            } '''
            ,'graph2':
            ''' {
                    "subject3": {
                        "predicate5": "singleobject3",
                        "predicate6": [ "multiobject5", "multiobject6" ]
                    },
                    "subject4": {
                        "predicate7": "singleobject4",
                        "predicate8": [ "multiobject7", "multiobject8" ]
                    }
            } '''
            , 'DEFAULT': '{ "subject5": { "predicate9": "singleobject5" } }'
            }

test_triples = list(((s, p, o) for (s, p, o, g) in quads if g == 'graph1'))
triplegraph = quadgraphs['graph1']


class TestRDFdict(unittest.TestCase):
    def test_quads(self):
        for (graphname, triples_as_dict) in RDFdict(quads=quads).graphs():
            test_dict = json.loads(quadgraphs[graphname])
            self.assertTrue(compare_dicts(test_dict, triples_as_dict))

    def test_add_triple(self):
        r = RDFdict()
        r.add_triple('s', 'p', 'o')
        triples_as_dict = r.default_graph()
        self.assertTrue(compare_dicts(json.loads('{"s": { "p": "o" } }'), triples_as_dict))

    def test_add_quad(self):
        r = RDFdict()
        r.add_quad('s', 'p', 'o', 'g')
        triples_as_dict = r.graph('g')
        self.assertTrue(compare_dicts(json.loads('{"s": { "p": "o" } }'), triples_as_dict))

    def test_triples(self):
        r = RDFdict(triples=test_triples)
        triples_as_dict = r.default_graph()
        self.assertTrue(compare_dicts(json.loads(triplegraph), triples_as_dict))

    def test_default_graph_name_DEFAULT(self):
        r = RDFdict(triples=test_triples)
        self.assertEqual(r.default_graph_name(), 'DEFAULT')

    def test_default_graph_name_foo(self):
        r = RDFdict(triples=test_triples, default_graph='foo')
        self.assertEqual(r.default_graph_name(), 'foo')

    def test_default_graph_in_graphs(self):
        r = RDFdict(triples=test_triples)
        for (name, graph) in r.graphs():
            self.assertEqual(name, 'DEFAULT')

    def test_default_graph_in_graphs_when_named(self):
        r = RDFdict(triples=test_triples, default_graph='foo')
        for (name, graph) in r.graphs():
            self.assertEqual(name, 'foo')


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