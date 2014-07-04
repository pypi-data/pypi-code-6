# coding:utf-8
import os
import unittest
from xml.etree import ElementTree
from casslr import szradm


class TestFarmRoleEngine(szradm.FarmRoleEngine):
    def __init__(self):
        self.responses = []
        self.params = []

    def _szradm(self, params):
        self.params.append(params)
        return ElementTree.fromstring(self.responses.pop(0))


class FarmRoleEngineTestCase(unittest.TestCase):
    def setUp(self):
        self.test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.engine = TestFarmRoleEngine()