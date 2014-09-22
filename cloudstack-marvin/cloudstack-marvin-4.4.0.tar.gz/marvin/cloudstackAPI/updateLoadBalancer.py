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


"""Updates a Load Balancer"""
from baseCmd import *
from baseResponse import *
class updateLoadBalancerCmd (baseCmd):
    def __init__(self):
        self.isAsync = "true"
        """the ID of the Load Balancer"""
        """Required"""
        self.id = None
        """an optional field, in case you want to set a custom id to the resource. Allowed to Root Admins only"""
        self.customid = None
        """an optional field, whether to the display the rule to the end user or not"""
        self.fordisplay = None
        self.required = ["id",]

class updateLoadBalancerResponse (baseResponse):
    def __init__(self):
        """the Load Balancer ID"""
        self.id = None
        """the account of the Load Balancer"""
        self.account = None
        """the load balancer algorithm (source, roundrobin, leastconn)"""
        self.algorithm = None
        """the description of the Load Balancer"""
        self.description = None
        """the domain of the Load Balancer"""
        self.domain = None
        """the domain ID of the Load Balancer"""
        self.domainid = None
        """is rule for display to the regular user"""
        self.fordisplay = None
        """the name of the Load Balancer"""
        self.name = None
        """Load Balancer network id"""
        self.networkid = None
        """the project name of the Load Balancer"""
        self.project = None
        """the project id of the Load Balancer"""
        self.projectid = None
        """Load Balancer source ip"""
        self.sourceipaddress = None
        """Load Balancer source ip network id"""
        self.sourceipaddressnetworkid = None
        """the list of instances associated with the Load Balancer"""
        self.loadbalancerinstance = []
        """the list of rules associated with the Load Balancer"""
        self.loadbalancerrule = []
        """the list of resource tags associated with the Load Balancer"""
        self.tags = []

class loadbalancerinstance:
    def __init__(self):
        """"the instance ID"""
        self.id = None
        """"the ip address of the instance"""
        self.ipaddress = None
        """"the name of the instance"""
        self.name = None
        """"the state of the instance"""
        self.state = None

class loadbalancerrule:
    def __init__(self):
        """"instance port of the load balancer rule"""
        self.instanceport = None
        """"source port of the load balancer rule"""
        self.sourceport = None
        """"the state of the load balancer rule"""
        self.state = None

class tags:
    def __init__(self):
        """"the account associated with the tag"""
        self.account = None
        """"customer associated with the tag"""
        self.customer = None
        """"the domain associated with the tag"""
        self.domain = None
        """"the ID of the domain associated with the tag"""
        self.domainid = None
        """"tag key name"""
        self.key = None
        """"the project name where tag belongs to"""
        self.project = None
        """"the project id the tag belongs to"""
        self.projectid = None
        """"id of the resource"""
        self.resourceid = None
        """"resource type"""
        self.resourcetype = None
        """"tag value"""
        self.value = None

