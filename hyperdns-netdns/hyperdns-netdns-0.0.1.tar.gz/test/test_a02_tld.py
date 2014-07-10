import unittest
import hyperdns.netdns as dns

class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_a00_(self):
        dns.validate_tld('com')
        


