#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

# =============================================================================
# DOC
# =============================================================================

"""yatel.etl module tests"""


# =============================================================================
# IMPORTS
# =============================================================================
import os
import tempfile
import shutil

from yatel import etl
from yatel import db
from yatel.tests.core import YatelTestCase
from yatel import dom

# =============================================================================
# VALIDATE TESTS
# =============================================================================
ETL = """

from yatel import etl, dom

class ETLTest(etl.BaseETL):

    def setup(self):
        self.hap1 = dom.Haplotype(1, arg="fa")
        self.fact1 = dom.Fact(1, attr0="fac")
        self.edge1 = dom.Edge(1, (1, 2))

    def haplotype_gen(self):
        return [self.hap1]

    def fact_gen(self):
        return [self.fact1]

    def edge_gen(self):
        return [self.edge1]
"""


class ETLTest(etl.BaseETL):

    def setup(self):
        self.hap1 = dom.Haplotype(1, arg="fa")
        self.hap2 = dom.Haplotype(2, arg="faaa")
        self.fact1 = dom.Fact(1, attr0="fac")
        self.fact2 = dom.Fact(2, attr0="facc")
        self.edge1 = dom.Edge(1, (1, 2))
        self.edge2 = dom.Edge(2, (1, 2))

    def haplotype_gen(self):
        return [self.hap1, self.hap2]

    def fact_gen(self):
        return [self.fact1, self.fact2]

    def edge_gen(self):
        return [self.edge1, self.edge2]


class TestEtl(YatelTestCase):

    def setUp(self):
        self.tempfile_path = tempfile.mkdtemp(prefix="yatel_test")
        self.nw = db.YatelNetwork("memory", mode="w")
        self.etl = ETLTest()
        self.lista = [1, 2]
        self.pth_with_etl = os.path.join(self.tempfile_path, "with_etl.py")
        self.pth_without_etl = os.path.join(self.tempfile_path,
                                            "without_etl.py")

    def tearDown(self):
        shutil.rmtree(self.tempfile_path)

    def test_scan_dir(self):
        with open(self.pth_with_etl, "w") as fp:
            fp.write(ETL)
        with open(self.pth_without_etl, "w") as fp:
            fp.write("")
        rs = etl.scan_dir(self.tempfile_path)

    def test_scan_file(self):
        with open(self.pth_with_etl, "w") as fp:
            fp.write(ETL)
        for content in os.listdir(self.tempfile_path):
            path = os.path.join(self.tempfile_path, content)
            rs = etl.scan_file(path)

    def test_execute(self):
        haplotype = [
            dom.Haplotype(1, arg="fa"),
            dom.Haplotype(2, arg="faaa")
        ]

        edge = [
            dom.Edge(1, (1, 2)),
            dom.Edge(2, (1, 2))
        ]
        fact = [
            dom.Fact(1, attr0="fac"),
            dom.Fact(2, attr0="facc")
        ]
        nw = db.YatelNetwork("memory", mode="w")
        nw.add_elements(haplotype + edge + fact)
        nw.confirm_changes()
        rs = etl.execute(self.nw, self.etl, )
        self.nw.confirm_changes()
        self.assertTrue(rs)
        self.assertSameUnsortedContent(nw.haplotypes(), self.nw.haplotypes())
        self.assertSameUnsortedContent(nw.facts(), self.nw.facts())
        self.assertSameUnsortedContent(nw.edges(), self.nw.edges())

    def test_etlcls_from_module(self):
        with open(self.pth_with_etl, "w") as fp:
            fp.write(ETL)
        for content in os.listdir(self.tempfile_path):
            path = os.path.join(self.tempfile_path, content)
        rs = etl.etlcls_from_module(path, "ETLTest")

    def test_get_template(self):
        rs = etl.get_template()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
