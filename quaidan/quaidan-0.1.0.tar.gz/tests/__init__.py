from quaidan import BalancerManager
import unittest

class BalancerManagerTest(unittest.TestCase):
    def test_reads_status(self):
        manager = BalancerManager('http://127.0.0.1/balancer-manager')
        status = manager.get_status()
        self.assertEquals('http://192.168.1.52', status.clusters[1].members[0].worker_url)
