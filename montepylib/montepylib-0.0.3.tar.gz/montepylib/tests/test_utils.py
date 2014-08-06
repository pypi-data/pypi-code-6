# you can run these tests with:
#   python tests.py
#
import os
import unittest

# add the parent directory to the path so the montepylib directory can be found
os.sys.path.append(os.path.dirname(os.path.abspath('.')))
from montepylib.utils import is_string_int

class Test1(unittest.TestCase):

    def test_is_string_int(self):
        self.assertTrue(is_string_int("2010"))
        self.assertFalse(bool(is_string_int("2010.")))
        self.assertRaises(AssertionError, is_string_int, 2010)


def main():
    unittest.main()

if __name__ == "__main__":# and __package__ is None:
    main()