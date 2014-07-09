import unittest
import mock

from libs.iRunnerPlugin import IRunnerPlugin

class TestIRunnerPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = IRunnerPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), "IRunnerPlugin actif")

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), "IRunnerPlugin inactif")
