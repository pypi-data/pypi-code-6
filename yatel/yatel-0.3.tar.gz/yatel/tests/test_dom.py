#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

# ===============================================================================
# DOC
# ===============================================================================

"""yatel.dom module tests"""


# ===============================================================================
# IMPORTS
# ===============================================================================

from yatel import dom
from yatel.tests.core import YatelTestCase


# ===============================================================================
# VALIDATE TESTS
# ===============================================================================

class TestHaplatoype(YatelTestCase):

    def test_getattr(self):
        hap1 = dom.Haplotype(1, arg="fa")
        self.assertEquals("fa", hap1.arg)
        self.assertEquals("fa", hap1["arg"])
        self.assertEquals(hap1.arg, hap1["arg"])

    def test_eq(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertEquals(hap0, hap1)

    def test_ne(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(2)
        self.assertNotEqual(hap0, hap1)

    def test_hash(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertEquals(hash(hap0), hash(hap1))

    def test_is(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, arg="foo")
        self.assertFalse(hap0 is hap1)
        self.assertTrue(hap0 is hap0)
        self.assertTrue(hap1 is hap1)

    def test_in(self):
        hap0 = dom.Haplotype(1)
        hap1 = dom.Haplotype(1, attr="foo")
        hap2 = dom.Haplotype(2)
        d = {hap0: "foo"}
        self.assertIn(hap0, d)
        self.assertIn(hap1, d)
        self.assertNotIn(hap2, d)
        d.update({hap1: "faa", hap2: "fee"})
        self.assertEquals(d[hap0], "faa")
        self.assertEquals(d[hap1], "faa")
        self.assertEquals(d[hap2], "fee")
        self.assertEquals(len(d), 2)

    def test_none_values(self):
        hap0 = dom.Haplotype(1, attr=None)
        self.assertRaises(AttributeError, lambda: hap0.attr)


class TestEdge(YatelTestCase):

    def test_getattr(self):
        edge0 = dom.Edge(1, (1, 2))
        self.assertEquals((1, 2), edge0.haps_id)
        self.assertEquals((1, 2), edge0["haps_id"])
        self.assertEquals(edge0.haps_id, edge0["haps_id"])

    def test_types(self):
        edge = dom.Edge("1", [1, 2])
        self.assertTrue(isinstance(edge.weight, float))
        self.assertTrue(isinstance(edge.haps_id, tuple))

    def test_eq(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 2])
        self.assertEquals(edge0, edge1)

    def test_ne(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(2, [1, 3])
        self.assertNotEqual(edge0, edge1)

    def test_hash(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 2])
        self.assertEquals(hash(edge0), hash(edge1))

    def test_is(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(2, [1, 3])
        self.assertFalse(edge0 is edge1)
        self.assertTrue(edge0 is edge0)
        self.assertTrue(edge1 is edge1)

    def test_in(self):
        edge0 = dom.Edge(1, [1, 2])
        edge1 = dom.Edge(1, [1, 4])
        edge2 = dom.Edge(2, [1, 3])
        d = {edge0: [1, 4]}
        self.assertIn(edge0, d)
        self.assertNotIn(edge1, d)
        self.assertNotIn(edge2, d)
        d.update({edge1: [1, 3], edge2: [1, 2]})
        self.assertEquals(d[edge0], [1, 4])
        self.assertEquals(d[edge1], [1, 3])
        self.assertEquals(d[edge2], [1, 2])
        self.assertEquals(len(d), 3)


class TestFact(YatelTestCase):
    def test_getattr(self):
        fact1 = dom.Fact(1, attr0="fac")
        self.assertEquals("fac", fact1.attr0)
        self.assertEquals("fac", fact1["attr0"])
        self.assertEquals(fact1.attr0, fact1["attr0"])

    def test_eq(self):
        fact0 = dom.Fact(1, attr0="fac")
        fact1 = dom.Fact(1, attr0="fac")
        self.assertEquals(fact0, fact1)

    def test_ne(self):
        fact0 = dom.Fact(1, attr0="fac", attr1="fact")
        fact1 = dom.Fact(2, attr0="fac", attr1="fact")
        self.assertNotEqual(fact0, fact1)

    def test_hash(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1)
        self.assertEquals(hash(fact0), hash(fact1))

    def test_is(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1, attr0="foo")
        self.assertFalse(fact0 is fact1)
        self.assertTrue(fact0 is fact0)
        self.assertTrue(fact1 is fact1)

    def test_in(self):
        fact0 = dom.Fact(1)
        fact1 = dom.Fact(1, attr0="foo")
        fact2 = dom.Fact(2)
        d = {fact0: "foo"}
        self.assertIn(fact0, d)
        self.assertNotIn(fact1, d)
        self.assertNotIn(fact2, d)
        d.update({fact1: "faa", fact2: "fee"})
        self.assertEquals(d[fact0], "foo")
        self.assertEquals(d[fact1], "faa")
        self.assertEquals(d[fact2], "fee")
        self.assertEquals(len(d), 3)

    def test_none_values(self):
        fact1 = dom.Fact(1, attr0="foo", attr1=None)
        self.assertRaises(AttributeError, lambda: fact1.attr1)


class TestEnvironment(YatelTestCase):

    def test_getattr(self):
        environment1 = dom.Environment(attr0="env")
        self.assertEquals("env", environment1.attr0)
        self.assertEquals("env", environment1["attr0"])
        self.assertEquals(environment1.attr0, environment1["attr0"])

    def test_eq(self):
        environment0 = dom.Environment(attr0="fac")
        environment1 = dom.Environment(attr0="fac")
        self.assertEquals(environment0, environment1)

    def test_ne(self):
        environment0 = dom.Environment(attr0="fac")
        environment1 = dom.Environment()
        self.assertNotEqual(environment0, environment1)

    def test_hash(self):
        environment0 = dom.Environment()
        environment1 = dom.Environment()
        self.assertEquals(hash(environment0), hash(environment1))

    def test_is(self):
        environment0 = dom.Environment(attr0="fac")
        environment1 = dom.Environment()
        self.assertFalse(environment0 is environment1)
        self.assertTrue(environment0 is environment0)
        self.assertTrue(environment1 is environment1)

    def test_in(self):
        environment0 = dom.Environment(attr0="fac")
        environment1 = dom.Environment()
        environment2 = dom.Environment()
        d = {environment0}
        self.assertIn(environment0, d)
        self.assertNotIn(environment1, d)
        self.assertNotIn(environment2, d)
        self.assertEquals(len(d), 1)

    def test_none_values(self):
        environment1 = dom.Environment(attr0=None)
        self.assertEquals(environment1.attr0, None)


class TestDescriptor(YatelTestCase):

    def test_getattr(self):
        descriptor1 = dom.Descriptor("env", None, None, None, None)
        self.assertEquals("env", descriptor1.mode)

    def test_eq(self):
        descriptor0 = dom.Descriptor(None, None, None, None, 3)
        descriptor1 = dom.Descriptor(None, None, None, None, 3)
        self.assertEquals(descriptor0, descriptor1)

    def test_ne(self):
        descriptor0 = dom.Descriptor("env", None, None, None, None)
        descriptor1 = dom.Descriptor(None, None, None, None, None)
        self.assertNotEqual(descriptor0, descriptor1)

    def test_hash(self):
        descriptor0 = dom.Descriptor(None, None, None, None, None)
        descriptor1 = dom.Descriptor(None, None, None, None, None)
        self.assertEquals(hash(descriptor0), hash(descriptor1))

    def test_is(self):
        descriptor0 = dom.Descriptor("env", None, None, None, None)
        descriptor1 = dom.Descriptor(None, None, None, None, None)
        self.assertFalse(descriptor0 is descriptor1)
        self.assertTrue(descriptor0 is descriptor0)
        self.assertTrue(descriptor1 is descriptor1)

    def test_in(self):
        descriptor0 = dom.Descriptor(None, None, None, None, None)
        descriptor1 = dom.Descriptor(None, None, None, None, 4)
        d = {descriptor0}
        self.assertIn(descriptor0, d)
        self.assertNotIn(descriptor1, d)
        self.assertEquals(len(d), 1)

    def test_none_values(self):
        descriptor1 = dom.Descriptor(None, None, None, None, None)
        self.assertEquals(descriptor1.mode, None)


# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print(__doc__)
