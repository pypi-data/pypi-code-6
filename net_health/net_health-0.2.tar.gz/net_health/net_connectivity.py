#!/usr/bin/env python
import sys
import ast

import logging

from neutronclient.v2_0 import client
from credentials import get_credentials
from credentials import get_nova_credentials_v2
from novaclient.client import Client
from remote_client import RemoteClient
from utils import NovaManageExec

LOG = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
LOG.addHandler(ch)
LOG.setLevel(logging.DEBUG)


def main(argv):
    src_instance_id = argv[0]
    NetworkHealthChecker(src_instance_id).check_network_connectivity()


class NetworkHealthChecker(object):

    def __init__(self, src_instance_id):
        neutron_credentials = get_credentials()
        self.neutron_client = client.Client(**neutron_credentials)
        nova_credentials = get_nova_credentials_v2()
        self.nova_client = Client(**nova_credentials)
        self.src_vm_instance_id = src_instance_id

    def check_network_connectivity(self):
        netw = self.neutron_client.list_networks(**
                                                 {'router:external': 'False'})
        netw_ids = [network['id'] for network in netw['networks']]
        src_ip_address = filter(lambda x: x.instance_id ==
                                self.src_vm_instance_id,
                                self.nova_client.floating_ips.list())[0].ip
        for net_id in netw_ids:
            for port in self.neutron_client.list_ports(
                    network_id=net_id, device_owner="compute:None")['ports']:
                self._check_tenant_network_connectivity(src_ip_address, port)
                self._check_public_network_connectivity(src_ip_address, port)

    def _get_host_id(self, instance_id=None):
        ports = self.neutron_client.list_ports(**{'device_id': instance_id})
        host_id = ports['ports'][0]['binding:host_id']
        return host_id

    def _check_tenant_network_connectivity(self, src_ip, target_vm_port):
        target_ip_address = target_vm_port['fixed_ips'][0]['ip_address']
        LOG.debug('checking internal network connections to IP %s' %
                  target_ip_address)
        try:
            internal_connectivity = self._check_vm_connectivity(
                src_ip, target_ip_address)
            if not internal_connectivity:
                host_id = target_vm_port['binding:host_id']
                self._check_host_connectivity(host_id)
        except Exception as e:
            LOG.error('Tenant network connectivity check failed: %s %', e)
            raise

    def _get_remote_client(self, dest_ip_address,  username):
        return RemoteClient(dest_ip_address, username)

    def _check_vm_connectivity(self, src_ip_address,
                               target_ip_address, username='ubuntu'):
        source_vm = self._get_remote_client(src_ip_address, username)

        LOG.debug("try pinging ip: %s" % target_ip_address)
        ping_success = source_vm.ping_host(target_ip_address)
        if ping_success:
            LOG.debug("ping success to ip: %s" % target_ip_address)
        else:
            LOG.error("Timed out waiting for %s to become reachable" %
                      target_ip_address)
        return ping_success

    def _get_host_ip_dict(self):
        nova_manage = NovaManageExec('get_host_ip_nova_manage_script.py')
        return nova_manage.call()[0]

    def _check_host_connectivity(self, host_id):
        host_name_ip_dict = self._get_host_ip_dict()
        src_host_id = self._get_host_id(self.src_vm_instance_id)
        src_host_ip = ast.literal_eval(host_name_ip_dict)[src_host_id]
        host_ip = ast.literal_eval(host_name_ip_dict)[host_id]
        LOG.debug("try pinging host: %s" % host_ip)
        return self._check_vm_connectivity(src_host_ip, host_ip, 'root')


#     not needed anymore - for local ping
#     def _ping_ip_address(self, ip_address):
#         cmd = ['ping', '-c1', '-w1', ip_address]
#         proc = subprocess.Popen(cmd,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE)
#         proc.wait()
#         return proc.returncode == 0
#
    def _check_public_network_connectivity(self,
                                           src_ip_address, target_vm_port):
        floating_ip = filter(lambda x: x.instance_id ==
                             target_vm_port['device_id'],
                             self.nova_client.floating_ips.list())[0].ip
        LOG.debug('checking extenal connections to IP %s' % floating_ip)
        try:
            self._check_vm_connectivity(src_ip_address, floating_ip)
        except Exception as e:
            LOG.error('Public network connectivity check failed: %s' % e)
            raise

if __name__ == "__main__":
    main(sys.argv[1:])
