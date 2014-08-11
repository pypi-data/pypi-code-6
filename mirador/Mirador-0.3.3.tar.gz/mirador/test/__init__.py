# test the mirador python package
import unittest
from test_client import suite as client_suite


def suite():
    return unittest.TestSuite([client_suite])


if __name__ == "__main__":
    unittest.main()
