from unittest import TestCase


class TestCase(TestCase):

    def assertListsEquivalent(self, list_one, list_two):
        """ Assert that the two lists contain the same data, regardless of order """
        self.assertEqual(sorted(list_one), sorted(list_two))
