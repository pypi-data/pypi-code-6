"""
Copyright (c) 2014 Maciej Nabozny

This file is part of OverCluster project.

OverCluster is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from pyCore.utils import request, calc_hash
from pyCore.models.base_model import BaseModel


class VPN(BaseModel):

    def delete(self):
        request(self.oc_address, '/vpn/network/delete/', {'token': self.token,
                                                          'vpn_id': self.id})

    def attach(self, vm):
        request(self.oc_address, '/vpn/network/attach/', {'token': self.token,
                                                          'vpn_id': self.id,
                                                          'vm_id': vm.id})

    def detach(self, vm):
        request(self.oc_address, '/vpn/network/detach/', {'token': self.token,
                                                          'vpn_id': self.id,
                                                          'vm_id': vm.id})

    def client_cert(self, vm):
        return request(self.oc_address, '/vpn/network/client_cert/', {'token': self.token,
                                                                      'vpn_id': self.id,
                                                                      'vm_id': vm.id})