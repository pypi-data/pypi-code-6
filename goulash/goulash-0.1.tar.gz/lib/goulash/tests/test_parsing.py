""" test_parsing """

import unittest

from goulash import parsing

class TestAnsi(unittest.TestCase):

    def setUp(self):
        pass

    def test_strip_tags(self):
        self.assertEqual(parsing.strip_tags('<div>foo</div>'),'foo')

    def test_sanitize(self):
        self.assertEqual(parsing.sanitize_txt('A B C'), 'a_b_c')

    def test_smart_split(self):
        tmp = parsing.smart_split('a_b-c.d')
        self.assertEqual(tmp,'a b c d'.split())
