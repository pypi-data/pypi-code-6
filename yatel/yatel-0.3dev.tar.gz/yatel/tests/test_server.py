#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.server module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random, json, tempfile, os, unittest

from jsonschema import ValidationError

from yatel import server, qbj, typeconv,db
from yatel.cluster import kmeans
from yatel.tests import test_qbj
from yatel.tests import core


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestYatelHttpServer(test_qbj.QBJEngineTest):

    def setUp(self):
        super(TestYatelHttpServer, self).setUp()
        self.testnw = "testnw"
        self.url = "/qbj/{}".format(self.testnw)
        self.server = server.YatelHttpServer(DEBUG=True)
        self.server.add_nw(self.testnw, self.nw, enable_qbj=True)
        self.app = self.server.test_client()

    def execute(self, query):
        data = json.dumps(query)
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', len(data))
        ]
        response = self.app.post(self.url, headers=headers, data=data)
        rs = json.loads(response.data)
        if rs["error"]:
            full_fail = "".join([rs["error_msg"], rs["stack_trace"]])
            self.fail(full_fail)
        return rs

    @unittest.skipUnless(core.MOCK, "require mock")
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


class TestServerFunctions(core.YatelTestCase):

    def test_validate_conf(self):
        vconf = json.loads(server.get_conf_template())
        self.assertIs(server.validate_conf(vconf), None)
        self.assertRaises(ValidationError, lambda: server.validate_conf(""))

    def test_get_conf_template(self):
        vconf = json.loads(server.get_conf_template())
        self.assertEquals(vconf, server.CONF_BASE)

    def test_from_dict(self):
        vconf = json.loads(server.get_conf_template())
        vconf["NETWORKS"]["network-name"]["uri"] = "memory:///"
        self.assertRaises(
            db.YatelNetworkError, lambda: server.from_dict(vconf)
        )
        try:
            fd, path = tempfile.mkstemp()
            conn = {"engine": "sqlite", "database": path}
            nw = self.get_random_nw(conn)[0]
            vconf["NETWORKS"]["network-name"]["uri"] = nw.uri
            srv = server.from_dict(vconf)
            self.assertEquals(srv.nw("network-name").describe(), nw.describe())
        except:
            raise
        finally:
            os.close(fd)

    def test_get_wsgi_template(self):
        try:
            fd, path = tempfile.mkstemp()
            wsgi = server.get_wsgi_template(path)
            self.assertEquals(
                wsgi, server.WSGI_BASE_TPL.substitute(confpath=path).strip()
            )
        except:
            raise
        finally:
            os.close(fd)

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
