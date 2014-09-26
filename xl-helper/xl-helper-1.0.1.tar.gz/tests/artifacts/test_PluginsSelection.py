import unittest

from xl_helper.artifacts.PluginsSelection import PluginsSelection
from xl_helper.artifacts.Plugin import Plugin


class PluginsSelectionTest(unittest.TestCase):

    was4_0 = Plugin("was-plugin-4.0.0.jar")
    was3_9 = Plugin("was-plugin-3.9.0.jar")
    wls4_0_snapshot = Plugin("wls-plugin-4.0.0-SNAPSHOT.jar")
    wls4_5 = Plugin("wls-plugin-4.5.0.jar")

    def test_no_duplicated_plugins(self):
        selection = PluginsSelection([self.was4_0, self.wls4_5])
        self.assertEqual(selection.get_outdated_plugins(), [])

    def test_some_duplicated_plugins(self):
        selection = PluginsSelection([
            self.was4_0,
            self.was3_9,
            self.wls4_0_snapshot,
            self.wls4_5
        ])

        self.assertEqual(
            selection.get_outdated_plugins(),
            [self.was3_9, self.wls4_0_snapshot]
        )