#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.client module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random, json, tempfile, os, unittest

from jsonschema import ValidationError

from yatel import client, qbj, typeconv, db
from yatel.cluster import kmeans
from yatel.tests import test_qbj
from yatel.tests import core


#===============================================================================
# VALIDATE TESTS
#===============================================================================

@unittest.skipUnless(core.MOCK, "require mock")
class TestQBJClient(test_qbj.QBJEngineTest):

    def setUp(self):
        super(TestQBJClient, self).setUp()
        self.client = client.QBJClient("http://localhost:8000", "test")

    def execute(self, query):
        response = self.client.execute(query)
        return super(TestQBJClient, self).execute(query)

    def test_kmeans(self):
        envs = map(dict, self.nw.environments(["native", "place"]))
        query = {
            "id": 1,
            "function": {
                "name": 'kmeans',
                "args": [
                    {"type": 'literal', "value": envs},
                    {"type": 'literal', "value": 2}
                ]
            }
        }
        orig = kmeans.kmeans(self.nw, envs=envs, k_or_guess=2)
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEquals(orig[0], rs[0])
        self.assertEquals(orig[1], rs[1])


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
