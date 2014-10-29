from hamcrest import *
from quaidan.client import Client
import random
import string
import unittest

class ClientTest(unittest.TestCase):

    def setUp(self):
        self._client = Client('http://127.0.0.1/balancer-manager')

    def test_get_balancer_manager_page(self):
        page = self._client.get_balancer_manager_page()
        assert_that(page, string_contains_in_order(
            '<h1>Load Balancer Manager for 127.0.0.1</h1>',
            '<address>Apache/2.4.10 (Ubuntu) Server at 127.0.0.1 Port 80</address>'))

    def test_send_form(self):
        self.__reset_cluster('cluster2')
        page = self._client.get_balancer_manager_page()
        form = create_for_with_defaults_for_cluster('cluster2')
        random_string = ''.join([random.choice(string.ascii_letters) for n in range(32)])
        form['b_ss'] = random_string
        self._client.send_form(form)
        page = self._client.get_balancer_manager_page()
        assert_that(page, contains_string(random_string))

    def test_boolean_has_changed(self):
        self.__reset_cluster('cluster2')
        form = create_for_with_defaults_for_cluster('cluster2')
        form['b_sforce'] = True
        self._client.send_form(form)
        page = self._client.get_balancer_manager_page()
        assert_that(page, contains_string('On'))

    def test_send_form_does_not_add_nonce_to_form(self):
        form = create_for_with_defaults_for_cluster('cluster1')
        self._client.send_form(form)
        assert_that(form, is_not(has_key('nonce')))

    def __reset_cluster(self, cluster):
        """Resets a cluster configuration to its default.

        :param cluster: The name of the cluster.
        """
        form = create_for_with_defaults_for_cluster(cluster)
        self._client.send_form(form)

def create_for_with_defaults_for_cluster(cluster):
    return {
        'b_lbm': 'byrequests',
        'b_tmo': 0,
        'b_max': 1,
        'b_sforce': False,
        'b_ss': '',
        'b': cluster
    }
