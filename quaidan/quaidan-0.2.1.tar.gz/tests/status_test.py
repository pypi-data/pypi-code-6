from quaidan.status import parse_balancer_manager_page
import unittest

class BalancerManagerParserTest(unittest.TestCase):

    def setUp(self):
        with open('tests/balancer-manager.2.4.7.html', 'r') as htmlFile:
            html = htmlFile.read()
            self.status = parse_balancer_manager_page(html)

    def test_finds_two_clusters(self):
        self.assertEqual(2, len(self.status.clusters))

    def test_extracts_name_of_cluster(self):
        self.assertEquals('cluster1', self.status.clusters[0].name)

    def test_finds_members(self):
        self.assertEquals(2, len(self.status.clusters[0].members))

    def test_extracts_worker_url_of_member(self):
        self.assertEquals('http://192.168.1.50', self.status.clusters[0].members[0].worker_url)

    def test_extracts_route_of_member(self):
        self.assertEquals('dummy route', self.status.clusters[0].members[0].route)

    def test_extracts_route_redirect_of_member(self):
        self.assertEquals('dummy route redirect', self.status.clusters[0].members[0].route_redirect)

    def test_extracts_load_factor_of_member(self):
        self.assertEquals(2, self.status.clusters[0].members[0].load_factor)

    def test_extracts_lb_set_of_member(self):
        self.assertEquals(3, self.status.clusters[0].members[0].lb_set)

    def test_detects_ignore_errors_of_member(self):
        self.assertEquals(True, self.status.clusters[0].members[1].ignore_errors)

    def test_detects_draining_mode_of_member(self):
        self.assertEquals(True, self.status.clusters[0].members[1].draining_mode)

    def test_detects_enabled_state_of_member(self):
        self.assertEquals(True, self.status.clusters[0].members[0].enabled)

    def test_detects_disabled_state_of_member(self):
        self.assertEquals(False, self.status.clusters[1].members[0].enabled)

    def test_detects_hot_standby_of_member(self):
        self.assertEquals(True, self.status.clusters[1].members[1].hot_standby)

    def test_extracts_elected_of_member(self):
        self.assertEquals(4, self.status.clusters[0].members[0].elected)

    def test_extracts_busy_of_member(self):
        self.assertEquals(5, self.status.clusters[0].members[0].busy)

    def test_extracts_load_of_member(self):
        self.assertEquals(6, self.status.clusters[0].members[0].load)

    def test_extracts_transferred_of_member(self):
        self.assertEquals('17M', self.status.clusters[0].members[0].transferred)

    def test_extracts_read_of_member(self):
        self.assertEquals('1.8G', self.status.clusters[0].members[0].read)

if __name__ == '__main__':
    unittest.main()

