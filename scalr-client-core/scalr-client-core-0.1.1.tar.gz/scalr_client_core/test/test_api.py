# coding:utf-8
import os
import unittest

from scalr_client_core.exception import APIError
from scalr_client_core.test.util import TestAPIClient


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

    def test_farm_get_details(self):
        with open(os.path.join(self.data_dir, "FarmGetDetails.xml")) as f:
            success = f.read()

        # Test success
        api_client = TestAPIClient((200, success))
        response = api_client.call("FarmGetDetails")

        self.assertEqual("19458", response["Farm"]["ID"])
        print response["FarmRoleSet"]
        self.assertEqual(5, len(response["FarmRoleSet"]))

    def test_set_unpacking(self):
        with open(os.path.join(self.data_dir, "FarmGetDetails.xml")) as f:
            success = f.read()

        api_client = TestAPIClient((200, success))
        response = api_client.call("FarmGetDetails")

        yarn_master = response["FarmRoleSet"][1]
        self.assertEqual("72885", yarn_master["ID"])
        self.assertEqual(0, len(yarn_master["ServerSet"]))

        hdfs_slaves = response["FarmRoleSet"][2]
        self.assertEqual("72886", hdfs_slaves["ID"])
        self.assertEqual(3, len(hdfs_slaves["ServerSet"]))

    def test_api_error_handling(self):
        with open(os.path.join(self.data_dir, "Error.xml")) as f:
            error = f.read()
        api_client = TestAPIClient((200, error))
        self.assertRaises(APIError, api_client.call, "FarmGetDetails")

    def test_http_error_handling(self):
        api_client = TestAPIClient((500, ""))
        self.assertRaises(APIError, api_client.call, "FarmGetDetails")

    def test_xml_error_handling(self):
        error = "Not valid XML"
        api_client = TestAPIClient((200, error))
        self.assertRaises(APIError, api_client.call, "FarmGetDetails")

