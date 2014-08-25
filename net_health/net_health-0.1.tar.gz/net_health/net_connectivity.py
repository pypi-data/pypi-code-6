#!/usr/bin/env python

import subprocess
import logging

from neutronclient.v2_0 import client
from credentials import get_credentials
from credentials import get_nova_credentials_v2
from novaclient.client import Client

LOG = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
LOG.addHandler(ch)

def main():
    NetworkHealthChecker().check_network_connectivity()

class NetworkHealthChecker(object):

    def __init__(self) :
        neutron_credentials = get_credentials()
        self.neutron_client = client.Client(**neutron_credentials)
        nova_credentials = get_nova_credentials_v2()
        self.nova_client = Client(**nova_credentials)

    def check_network_connectivity(self):
        netw = self.neutron_client.list_networks(**
                    {'router:external':'False'})['networks']
        netw_ids = [ network['id'] for network in netw ]
        for net_id in netw_ids:
            for port in self.neutron_client.list_ports(network_id=net_id, 
                            device_owner="compute:None")['ports']:
                                self._check_tenant_network_connectivity(port)
                                self._check_public_network_connectivity(port)

    def _check_tenant_network_connectivity(self, compute_port):
        try:
            ip_address =  compute_port['fixed_ips'][0]['ip_address'] 
            LOG.debug('checking internal network connections to IP %s' % ip_address )
            self._check_vm_connectivity(ip_address)
        except Exception as e:
            LOG.error('Tenant network connectivity check failed')
            raise

    def _check_vm_connectivity(self, ip_address):
        """
        :param ip_address: server to test against

        :raises: AssertError if the result of the connectivity check does
            not match the value of the should_connect param
        """
        LOG.debug("try pinging ip: %s" % ip_address)
        if not self._ping_ip_address(ip_address):
            LOG.error("Timed out waiting for %s to become reachable" % ip_address)
        LOG.debug("ping success to ip: %s" % ip_address)

            
    def _ping_ip_address(self, ip_address):
        cmd = ['ping', '-c1', '-w1', ip_address]
        proc = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        proc.wait()
        return proc.returncode == 0

    def _check_public_network_connectivity(self, compute_port):
        floating_ip = filter(lambda x:x.instance_id == 
                compute_port['device_id'], 
                self.nova_client.
                floating_ips.list())[0].ip

        LOG.debug('checking extenal connections to IP %s' % floating_ip )
        try:
            self._check_vm_connectivity(floating_ip)
        except Exception as e:
            LOG.error('Public network connectivity check failed')
            raise

if __name__ == "__main__":
    main()
