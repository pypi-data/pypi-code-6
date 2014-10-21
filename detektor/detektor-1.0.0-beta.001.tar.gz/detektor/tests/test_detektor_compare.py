import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import detektor

import test_helpers


class TestDetektorCompare(unittest.TestCase):
    def setUp(self):
        self.a1 = test_helpers.Assignment('detektor/tests/pyfiles/helloworldplus.py')
        self.a2 = test_helpers.Assignment('detektor/tests/pyfiles/helloworldplus2.py')
        self.assignments = [self.a1, self.a2]
        detektor.set_detektor_signature('python', self.assignments, 'fileclass.filepath')

    def test_compare_2_equal_files(self):
        detektor.compare(self.assignments)
        self.assertTrue(hasattr(self.a1, 'detektor_signature'))

    def test_compare_but_sending_empty_list(self):
        res = detektor.compare([])
        self.assertTrue(type(res) == list)
        self.assertEqual(len(res), 0)

    def test_compare_3_equal_files(self):
        a3 = test_helpers.Assignment('detektor/tests/pyfiles/helloworldplus3.py')
        self.assignments.append(a3)
        detektor.set_detektor_signature('python', self.assignments, 'fileclass.filepath')
        res = detektor.compare(self.assignments)
        self.assertEqual(len(res), 3)

    def test_compare_4_equal_files(self):
        a3 = test_helpers.Assignment('detektor/tests/pyfiles/helloworldplus3.py')
        self.assignments.append(a3)
        a4 = test_helpers.Assignment('detektor/tests/pyfiles/helloworldplus4.py')
        self.assignments.append(a4)
        detektor.set_detektor_signature('python', self.assignments, 'fileclass.filepath')
        res = detektor.compare(self.assignments)
        self.assertEqual(len(res), 6)
