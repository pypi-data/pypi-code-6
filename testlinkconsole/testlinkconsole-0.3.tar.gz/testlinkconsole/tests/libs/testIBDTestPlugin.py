import unittest
import mock

from libs.iBDTestPlugin import IBDTestPlugin

class TestIBDTestPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = IBDTestPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), "IBDTestPlugin actif")

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), "IBDTestPlugin inactif")
