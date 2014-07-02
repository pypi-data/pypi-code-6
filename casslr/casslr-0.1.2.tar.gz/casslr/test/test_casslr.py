# coding:utf-8
import os

from casslr.app import app

from casslr.test.util import FarmRoleEngineTestCase


class CasslrTestCase(FarmRoleEngineTestCase):
    def setUp(self):
        super(CasslrTestCase, self).setUp()

        for response in ["user-data.xml", "roles-valid.xml"]:
            with open(os.path.join(self.test_data, response)) as f:
                self.engine.responses.append(f.read())

        app.config["ENGINE"] = self.engine
        self.client = app.test_client()

    def test_seeds(self):
        response = self.client.get('/seeds')
        self.assertEqual(200, response.status_code)

        seeds = response.data.decode("utf-8").split(",")
        self.assertEqual(3, len(seeds))

        self.assertEqual(set(("10.190.214.199", "10.157.42.56", "10.160.20.42")), set(seeds))
