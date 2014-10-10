from hamcrest import *
from quaidan.client import Client
import unittest

class ClientTest(unittest.TestCase):

    def setUp(self):
        self._client = Client('http://127.0.0.1/balancer-manager')

    def test_get_balancer_manager_page(self):
        page = self._client.get_balancer_manager_page()
        assert_that(page, string_contains_in_order(
            '<h1>Load Balancer Manager for 127.0.0.1</h1>',
            '<address>Apache/2.4.10 (Ubuntu) Server at 127.0.0.1 Port 80</address>'))
