""" goulash.tests.test_net

    WARNING: mocking sockets is sketchy as far portability and producing
             useful tests, so lots of these are integration tests, not
             unittests. (i.e. they might fail without a working network)
"""

import mock
import unittest
from goulash import net

class TestNet(unittest.TestCase):

    @mock.patch('socket.gethostbyname')
    def test_ipaddr_basic(self, get_host_by_name):
        get_host_by_name.return_value = 'fake'
        self.assertEqual(set(['fake']), net.ipaddr_basic())

    def test_is_port_open(self):
        self.assertFalse(net.is_port_open('fake-host', 22))

    def test_ipaddr_with_LAN(self):
        # super primitive test:
        # uses the network AND assumes ipv4
        ip = net.ipaddr_with_LAN()
        dots = [x for x in ip if x=='.']
        self.assertEqual(len(dots), 3)

    def test_ipaddr_hosts(self):
        hostname,aliases,ips = net.ipaddr_hosts()
        self.assertTrue(isinstance(hostname, basestring))
        self.assertTrue(isinstance(aliases, list))
        self.assertTrue(isinstance(ips, list))
