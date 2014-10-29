from quaidan import BalancerManager
from quaidan.command import UpdateMember
import unittest

class BalancerManagerTest(unittest.TestCase):
    def test_reads_status(self):
        manager = BalancerManager('http://127.0.0.1/balancer-manager')
        status = manager.get_status()
        self.assertEquals('http://192.168.1.52', status.clusters[1].members[0].worker_url)

    def test_updates_member(self):
        manager = BalancerManager('http://127.0.0.1/balancer-manager')
        status = manager.get_status()
        cluster = status.clusters[1]
        update_member = UpdateMember(cluster.name, cluster.members[0])
        update_member.route = 'dummy_route'
        update_member.route_redirect = 'dummy_route_redirect'
        update_member.load_factor = 1
        update_member.lb_set = 1
        update_member.ignore_errors = True
        update_member.draining_mode = True
        update_member.enabled = True
        update_member.hot_standby = True
        manager.send_command(update_member)
        
        status = manager.get_status()
        member = status.clusters[1].members[0]
        self.assertEquals('dummy_route', member.route)
        self.assertEquals('dummy_route_redirect', member.route_redirect)
        self.assertEquals(1, member.load_factor)
        self.assertEquals(1, member.lb_set)
        self.assertEquals(True, member.ignore_errors)
        self.assertEquals(True, member.draining_mode)
        self.assertEquals(True, member.enabled)
        self.assertEquals(True, member.hot_standby)
