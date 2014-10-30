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
        self.__verify_form_leads_to_page(form,
            contains_string(random_string))

    def test_boolean_has_changed(self):
        self.__reset_cluster('cluster2')
        form = create_for_with_defaults_for_cluster('cluster2')
        form['b_sforce'] = True
        self.__verify_form_leads_to_page(form,
            contains_string('On'))

    def test_None_string_is_replaced_with_empty_string(self):
        #we neeed a member form because cluster forms have no string
        #that can be used for testing
        form = {
            'b': 'cluster1',
            'w': 'http://192.168.1.50',
            'w_wr': None,
            'w_rr': None,
            'w_lf': 1,
            'w_ls': 1,
            'w_status_I': False,
            'w_status_N': False,
            'w_status_D': True,
            'w_status_H': False
        }
        self.__verify_form_leads_to_page(form,
            is_not(contains_string('<td>None')))

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

    def __verify_form_leads_to_page(self, form, matcher):
        self._client.send_form(form)
        page = self._client.get_balancer_manager_page()
        assert_that(page, matcher)

def create_for_with_defaults_for_cluster(cluster):
    return {
        'b_lbm': 'byrequests',
        'b_tmo': 0,
        'b_max': 1,
        'b_sforce': False,
        'b_ss': '',
        'b': cluster
    }
