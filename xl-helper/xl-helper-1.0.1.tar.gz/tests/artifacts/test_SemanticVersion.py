import unittest

from xl_helper.artifacts.SemanticVersion import SemanticVersion


class SemanticVersionTest(unittest.TestCase):

    def test_detect_snapshot(self):
        self.assertTrue(SemanticVersion("1.2.3-SNAPSHOT").snapshot)

    def test_compare_semantic_versions(self):
        self.assertTrue(SemanticVersion("3.9.4").less_than(SemanticVersion("4.0.0")))
        self.assertFalse(SemanticVersion("4.0.0").less_than(SemanticVersion("3.9.4")))

        self.assertTrue(SemanticVersion("1.2.3").less_than(SemanticVersion("2.2.3")))
        self.assertFalse(SemanticVersion("2.2.3").less_than(SemanticVersion("1.2.3")))

        self.assertTrue(SemanticVersion("1.2.3").less_than(SemanticVersion("1.3.3")))
        self.assertFalse(SemanticVersion("1.3.3").less_than(SemanticVersion("1.2.3")))

        self.assertTrue(SemanticVersion("1.2.3").less_than(SemanticVersion("1.2.4")))
        self.assertFalse(SemanticVersion("1.2.4").less_than(SemanticVersion("1.2.3")))

        self.assertTrue(SemanticVersion("1.2.3-SNAPSHOT").less_than(SemanticVersion("1.2.3")))
        self.assertFalse(SemanticVersion("1.2.3").less_than(SemanticVersion("1.2.3-SNAPSHOT")))
