import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import detektor

signature_keys = [
    'bigstring',
    'bigstringhash',
    'number_of_keywords',
    'list_of_functions',
    'number_of_operators',
    'keywordstring',
    'operatorstring',
]


class TestGetDetektorSignatureFromFile(unittest.TestCase):
    def setUp(self):
        self.filepath = 'detektor/tests/pyfiles/helloworldplus.py'

    def test_get_detektor_signature_from_file(self):
        sign = detektor.get_detektor_signature_from_file('python', self.filepath)
        self.assertEqual(type(sign), dict)

    def test_get_detektor_signature_from_file_has_all_keys(self):
        sign = detektor.get_detektor_signature_from_file('python', self.filepath)
        for key in signature_keys:
            self.assertTrue(key in sign)

    def test_get_detektor_signature_from_file_file_does_not_exist(self):
        with self.assertRaises(IOError):
            detektor.get_detektor_signature_from_file('python', 'this/file/does/not/exist.py')
