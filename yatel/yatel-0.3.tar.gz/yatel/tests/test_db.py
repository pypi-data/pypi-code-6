#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#==============================================================================
# DOC
#==============================================================================

"""yatel.db module tests"""


#==============================================================================
# IMPORTS
#==============================================================================

import os
import random
import string
import tempfile

from yatel import db, dom

from yatel.tests.core import YatelTestCase


#==============================================================================
# VALIDATE TESTS
#==============================================================================

class TestDBFunctions(YatelTestCase):

    def setUp(self):
        self.haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        self.edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        self.facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        self.nw = db.YatelNetwork("memory", mode="w")
        self.nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.nw.confirm_changes()

    def test_copy(self):
        anw = db.YatelNetwork(engine="memory", mode=db.MODE_WRITE)
        db.copy(self.nw, anw)
        anw.confirm_changes()
        for method in ["haplotypes", "facts", "edges"]:
            nw_values = getattr(self.nw, method)()
            anw_values = getattr(anw, method)()
            self.assertSameUnsortedContent(nw_values, anw_values)
        self.assertEquals(self.nw.describe(), anw.describe())

    def test_parse_uri(self):
        for mode in db.MODES:
            for log in [True, False]:
                parsed = db.parse_uri(
                    "engine://user:password@host:666/db", mode=mode, log=log
                )
                self.assertEquals(parsed["engine"], "engine")
                self.assertEquals(parsed["host"], "host")
                self.assertEquals(parsed["port"], 666)
                self.assertEquals(parsed["user"], "user")
                self.assertEquals(parsed["password"], "password")
                self.assertEquals(parsed["mode"], mode)
                self.assertEquals(parsed["log"], log)

    def test_to_uri(self):
        for eng in db.ENGINES:
            for mode in db.MODES:
                for log in [True, False]:
                    conf = dict(
                        (k, "foo") for k in db.ENGINE_VARS[eng]
                    )
                    conf["mode"] = mode
                    conf["log"] = log
                    if "port" in conf:
                        conf["port"] = 666

                    orig = string.Template(
                        db.ENGINE_URIS[eng]
                    ).safe_substitute(engine=eng, **conf)
                    uri = db.to_uri(engine=eng, **conf)
                    self.assertEquals(orig, uri)

    def test_exists(self):
        try:
            fd, ftemp = tempfile.mkstemp()
            self.assertFalse(db.exists("sqlite", database=ftemp))
        except:
            raise
        finally:
            os.close(fd)
        try:
            fd, ftemp = tempfile.mkstemp()
            self.get_random_nw({"engine": "sqlite", "database": ftemp})
            self.assertTrue(db.exists("sqlite", database=ftemp))
        except:
            raise
        finally:
            os.close(fd)

    def test_qfilter(self):
        query = list(
            db.qfilter(self.nw.haplotypes(), lambda hap: hap.get("age") == 200)
        )
        self.assertEquals(len(query), 1)
        self.assertEquals(query[0].hap_id, 0)


#==============================================================================
# NETWORK
#==============================================================================

class YatelNetwork(YatelTestCase):

    def setUp(self):
        self.haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        self.edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        self.facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        self.nw = db.YatelNetwork("memory", mode="w")
        self.nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.nw.confirm_changes()

    def add_element_elements(self):
        haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        for cont in [haplotypes, edges, facts]:
            for elem in cont:
                self.nw.add_element(elem)
        nw.confirm_changes()
        self.assertEquals(nw.describe(), self.nw.describe())
        self.assertSameUnsortedContent(nw.haplotypes(), self.nw.haplotypes())
        self.assertSameUnsortedContent(nw.facts(), self.nw.facts())
        self.assertSameUnsortedContent(nw.edges(), self.nw.edges())
        self.assertSameUnsortedContent(nw.environments(), self.nw.environments())

    def test_confirm_changes(self):
        haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        nw.add_elements(self.haplotypes + self.edges + self.facts)
        try:
            self.assertEquals(nw.describe(), self.nw.describe())
            self.assertSameUnsortedContent(
                nw.haplotypes(), self.nw.haplotypes()
            )
            self.assertSameUnsortedContent(nw.facts(), self.nw.facts())
            self.assertSameUnsortedContent(nw.edges(), self.nw.edges())
            self.assertSameUnsortedContent(
                nw.environments(), self.nw.environments()
            )
        except AttributeError:
            pass
        else:
            self.fail("No AttributeError in no confirmed networ")
        nw.confirm_changes()
        self.assertEquals(nw.describe(), self.nw.describe())
        self.assertSameUnsortedContent(nw.haplotypes(), self.nw.haplotypes())
        self.assertSameUnsortedContent(nw.facts(), self.nw.facts())
        self.assertSameUnsortedContent(nw.edges(), self.nw.edges())
        self.assertSameUnsortedContent(nw.environments(), self.nw.environments())

    def test_edges(self):
        self.assertSameUnsortedContent(self.nw.edges(), self.edges)

    def test_haplotypes(self):
        self.assertSameUnsortedContent(self.nw.haplotypes(), self.haplotypes)

    def test_facts(self):
        self.assertSameUnsortedContent(self.nw.facts(), self.facts)

    def test_describe(self):
        desc = self.nw.describe()
        self.assertEquals(desc["mode"], db.MODE_READ)
        self.assertEquals(desc["size"]["facts"], len(self.facts))
        self.assertEquals(desc["size"]["edges"], len(self.edges))
        self.assertEquals(desc["size"]["haplotypes"], len(self.haplotypes))
        for a, t in desc["haplotype_attributes"].items():
            for hap in self.haplotypes:
                if a in hap:
                    self.assertTrue(isinstance(hap[a], t))
        for a, t in desc["fact_attributes"].items():
            for fact in self.facts:
                if a in fact:
                    self.assertTrue(isinstance(fact[a], t))
        max_nodes = desc["edge_attributes"]["max_nodes"]
        wt = desc["edge_attributes"]["weight"]
        for edge in self.edges:
            self.assertTrue(len(edge.haps_id) <= max_nodes)
            self.assertTrue(isinstance(edge.weight, wt))

    def test_edges_by_environment(self):
        rs = list(self.nw.edges_by_environment(name="Andalucia"))
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0], self.edges[2])

    def test_facts_by_environment(self):
        rs = list(self.nw.facts_by_environment(name="Andalucia"))
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0], self.facts[0])
        self.assertEqual(rs[1], self.facts[3])

    def test_haplotypes_by_environment(self):
        rs = list(self.nw.haplotypes_by_environment(name="Andalucia"))
        self.assertEqual(len(rs), 2)
        self.assertEqual(rs[0], self.haplotypes[0])
        self.assertEqual(rs[1], self.haplotypes[2])

    def test_environments(self):
        desc = self.nw.describe()
        fact_attrs = desc["fact_attributes"].keys()
        for size in xrange(0, len(fact_attrs)):
            filters = set()
            while len(filters) < size:
                f = random.choice(fact_attrs)
                if f != "hap_id":
                    filters.add(f)
            list(self.nw.environments(list(filters)))

    def test_edges_by_haplotype(self):
        for hap in self.haplotypes:
            for edge in self.nw.edges_by_haplotype(hap):
                self.assertIn(hap.hap_id, edge.haps_id)

    def test_facts_by_haplotype(self):
        for hap in self.haplotypes:
            for fact in self.nw.facts_by_haplotype(hap):
                self.assertEquals(hap.hap_id, fact.hap_id)

    def test_haplotype_by_id(self):
        for hap in self.haplotypes:
            self.assertEquals(hap, self.nw.haplotype_by_id(hap.hap_id))

    def test_execute(self):
        rs = self.nw.execute("select * from {}".format(db.HAPLOTYPES))
        for row in rs:
            hap = self.nw.haplotype_by_id(row.hap_id)
            for k, v in row.items():
                if k in hap:
                    self.assertEquals(v, hap[k])
                else:
                    self.assertEquals(v, None)

    def test_mode(self):
        haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.assertEquals(nw.mode, db.MODE_WRITE)
        nw.confirm_changes()
        self.assertEquals(nw.mode, db.MODE_READ)

        try:
            fd, ftemp = tempfile.mkstemp()
            nw, haps = self.get_random_nw(
                {"engine": "sqlite", "database": ftemp}
            )
            nw = db.YatelNetwork(
                mode="a", **{"engine": "sqlite", "database": ftemp}
            )
            self.assertEquals(nw.mode, db.MODE_APPEND)
            nw.confirm_changes()
            self.assertEquals(nw.mode, db.MODE_READ)
        except:
            raise
        finally:
            os.close(fd)

        self.assertRaises(
            db.YatelNetworkError, lambda: db.YatelNetwork("memory", mode="a")
        )

    def test_uri(self):
        try:
            fd, ftemp = tempfile.mkstemp()
            nw, haps = self.get_random_nw(
                {"engine": "sqlite", "database": ftemp}
            )
            self.assertEquals(
                nw.uri, db.to_uri(**{"engine": "sqlite", "database": ftemp})
            )
        except:
            raise
        finally:
            os.close(fd)

    def test_validate_read(self):
        haplotypes = [
            dom.Haplotype(0, name="Cordoba", clima="calor", age=200),
            dom.Haplotype(1, name="Cordoba", population=12),
            dom.Haplotype(2, name="Cordoba")
        ]
        edges = [
            dom.Edge(6599, (0, 1)),
            dom.Edge(8924, (1, 2)),
            dom.Edge(9871, (2, 0))
        ]
        facts = [
            dom.Fact(0, name="Andalucia", lang="sp", timezone="utc-3"),
            dom.Fact(1, lang="sp"),
            dom.Fact(1, timezone="utc-6"),
            dom.Fact(2, name="Andalucia", lang="sp", timezone="utc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        nw.add_elements(self.haplotypes + self.edges + self.facts)
        self.assertRaises(db.YatelNetworkError, nw.validate_read)
        nw.confirm_changes()
        self.assertEquals(nw.validate_read(), None)

        try:
            fd, ftemp = tempfile.mkstemp()
            nw, haps = self.get_random_nw(
                {"engine": "sqlite", "database": ftemp}
            )
            nw = db.YatelNetwork(
                mode="a", **{"engine": "sqlite", "database": ftemp}
            )
            self.assertRaises(db.YatelNetworkError, nw.validate_read)
            nw.confirm_changes()
            self.assertEquals(nw.validate_read(), None)
        except:
            raise
        finally:
            os.close(fd)

    def test_append(self):
        try:
            fd, ftemp = tempfile.mkstemp()
            nw, haps = self.get_random_nw(
                {"engine": "sqlite", "database": ftemp}
            )
            new_haps = [dom.Haplotype(100)]
            new_facts = [dom.Fact(100, faa="foo")]
            new_edges = [dom.Edge(19, [100, 100])]

            for hap in nw.haplotypes():
                self.assertIn(hap.hap_id, haps)
                self.assertNotIn(hap, new_haps)
            for fact in nw.facts():
                self.assertIn(fact.hap_id, haps)
                self.assertNotIn(fact.hap_id, [f.hap_id for f in new_haps])
            for edge in nw.edges():
                for hap_id in edge.haps_id:
                    self.assertIn(hap_id, haps)
                    self.assertNotIn(hap_id, [h.hap_id for h in new_haps])

            nw = db.YatelNetwork(
                mode="a", **{"engine": "sqlite", "database": ftemp}
            )
            nw.add_elements(new_haps + new_facts + new_edges)
            nw.confirm_changes()

            for hap in nw.haplotypes():
                if hap not in new_haps:
                    self.assertIn(hap.hap_id, haps)
                else:
                    self.assertIn(hap, new_haps)
            for fact in nw.facts():
                if fact not in new_facts:
                    self.assertIn(fact.hap_id, haps)
                else:
                    self.assertIn(fact.hap_id, [f.hap_id for f in new_haps])
            for edge in nw.edges():
                for hap_id in edge.haps_id:
                    if edge not in new_edges:
                        self.assertIn(hap_id, haps)
                    else:
                        self.assertIn(hap_id, [h.hap_id for h in new_haps])
        except:
            raise
        finally:
            os.close(fd)

    def test_write(self):
        try:
            fd, ftemp = tempfile.mkstemp()
            nw, haps = self.get_random_nw(
                {"engine": "sqlite", "database": ftemp}
            )
            new_haps = [dom.Haplotype(100)]
            new_facts = [dom.Fact(100, faa="foo")]
            new_edges = [dom.Edge(19, [100, 100])]

            for hap in nw.haplotypes():
                self.assertIn(hap.hap_id, haps)
                self.assertNotIn(hap, new_haps)
            for fact in nw.facts():
                self.assertIn(fact.hap_id, haps)
                self.assertNotIn(fact.hap_id, [f.hap_id for f in new_haps])
            for edge in nw.edges():
                for hap_id in edge.haps_id:
                    self.assertIn(hap_id, haps)
                    self.assertNotIn(hap_id, [h.hap_id for h in new_haps])

            nw = db.YatelNetwork(
                mode="w", **{"engine": "sqlite", "database": ftemp}
            )
            nw.add_elements(new_haps + new_facts + new_edges)
            nw.confirm_changes()
            for hap in nw.haplotypes():
                self.assertIn(hap, new_haps)
            for fact in nw.facts():
                self.assertIn(fact.hap_id, [f.hap_id for f in new_haps])
            for edge in nw.edges():
                for hap_id in edge.haps_id:
                    self.assertIn(hap_id, [h.hap_id for h in new_haps])
        except:
            raise
        finally:
            os.close(fd)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
