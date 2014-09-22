# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


"""List all virtual machine instances that are assigned to a load balancer rule."""
from baseCmd import *
from baseResponse import *
class listLoadBalancerRuleInstancesCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """the ID of the load balancer rule"""
        """Required"""
        self.id = None
        """true if listing all virtual machines currently applied to the load balancer rule; default is true"""
        self.applied = None
        """List by keyword"""
        self.keyword = None
        """true if lb rule vm ip information to be included; default is false"""
        self.lbvmips = None
        """"""
        self.page = None
        """"""
        self.pagesize = None
        self.required = ["id",]

class listLoadBalancerRuleInstancesResponse (baseResponse):
    def __init__(self):
        """IP addresses of the vm set of lb rule"""
        self.lbvmipaddresses = None
        """the user vm set for lb rule"""
        self.loadbalancerruleinstance = None

