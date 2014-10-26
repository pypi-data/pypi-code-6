# Copyright (c) 2014 Monty Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from ironicclient import client as ironic_client
from ironicclient import exceptions as ironic_exceptions

from shade.user import cloud


class OperatorCloud(cloud.OpenStackCloud):


    def __init__(self, cloud, **kwargs):
        super(OperatorCloud, self).__init__(
            cloud, **kwargs)

        self.private = kwargs.get('private', True)
        self.endpoint_type = kwargs.get('endpoint_type', 'privateURL')
        self.on_behalf_of = kwargs.get('on_behalf_of', self.project_name)

    @property
    def ironic_client(self):
        if self._ironic_client is None:
            ironic_logging = logging.getLogger('ironicclient')
            ironic_logging.addHandler(logging.NullHandler())
            token = self.keystone_client.auth_token
            endpoint = self.get_endpoint(service_type='baremetal')
            try:
                self._ironic_client = ironic_client.Client(
                    '1', endpoint, token=token)
            except Exception as e:
                raise OpenStackCloudException(
                    "Error in connecting to ironic: %s" % e.message)
        return self._ironic_client

    def list_nics(self):
        return self.ironic_client.port.list()

    def get_nic_by_mac(self, mac):
        try:
            return self.ironic_client.port.get(mac)
        except ironic_exceptions.ClientException:
            return None

    def list_machines(self):
        return self.ironic_client.node.list()

    def get_machine_by_uuid(self, uuid):
        try:
            return self.ironic_client.node.get(uuid)
        except ironic_exceptions.ClientException:
            return None

    def get_machine_by_mac(self, mac):
        try:
            port = self.ironic_client.port.get(mac)
            return self.ironic_client.node.get(port.node_uuid)
        except ironic_exceptions.ClientException:
            return None

    def create_machine(self, **kwargs):
        return self.ironic_client.node.create(**kwargs)

    def delete_machine(self, uuid):
        return self.ironic_client.node.delete(uuid)
