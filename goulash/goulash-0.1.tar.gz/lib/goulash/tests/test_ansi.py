""" test_ansi.py """
import unittest

from goulash.ansi import Ansi2HtmlConverter


class TestAnsi(unittest.TestCase):
    def setUp(self):
        self.ansi = Ansi2HtmlConverter()

    def test_basic(self):
        self.assertTrue(self.ansi.get_style())
        self.assertEqual('foo', self.ansi.convert('foo'))
