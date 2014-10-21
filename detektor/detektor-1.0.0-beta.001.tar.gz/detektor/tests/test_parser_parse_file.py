import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detektor.libs.codeparser import Parser


class TestParserParseFile(unittest.TestCase):

    def setUp(self):
        self.testfilehandler = open('detektor/tests/pyfiles/helloworldplus.py', 'r')
        self.p = Parser('python', self.testfilehandler)

    def tearDown(self):
        self.testfilehandler.close()

    def test_get_python_content_keywordstring(self):
        self.assertIsInstance(self.testfilehandler, file)
        kwh, oph, bigstring, bigstring_hash, num_kw, num_op = self.p.parse_file()
        self.assertEqual(kwh, '_0_0_0_0_0_1_0_0_0_0_0_0_0_0_0_0_1_0_0_0_0_0_0_2_0_1_0_0_0')

    def test_get_python_operatorstring(self):
        kwh, oph, bigstring, bigstring_hash, num_kw, num_op = self.p.parse_file()
        self.assertEqual(oph, '_0_2_0_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0')

    def test_get_python_bigstring(self):
        kwh, oph, bigstring, bigstring_hash, num_kw, num_op = self.p.parse_file()
        self.assertEqual(bigstring_hash, -7070753577415992373)

    def test_get_python_number_of_keywords(self):
        kwh, oph, bigstring, bigstring_hash, num_kw, num_op = self.p.parse_file()
        self.assertEqual(num_kw, 5)

    def test_get_python_number_of_operators(self):
        kwh, oph, bigstring, bigstring_hash, num_kw, num_op = self.p.parse_file()
        self.assertEqual(num_op, 3)
