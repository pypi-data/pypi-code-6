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


"""lists Palo Alto firewall devices in a physical network"""
from baseCmd import *
from baseResponse import *
class listPaloAltoFirewallsCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """Palo Alto firewall device ID"""
        self.fwdeviceid = None
        """List by keyword"""
        self.keyword = None
        """"""
        self.page = None
        """"""
        self.pagesize = None
        """the Physical Network ID"""
        self.physicalnetworkid = None
        self.required = []

class listPaloAltoFirewallsResponse (baseResponse):
    def __init__(self):
        """device capacity"""
        self.fwdevicecapacity = None
        """device id of the Palo Alto firewall"""
        self.fwdeviceid = None
        """device name"""
        self.fwdevicename = None
        """device state"""
        self.fwdevicestate = None
        """the management IP address of the external firewall"""
        self.ipaddress = None
        """the number of times to retry requests to the external firewall"""
        self.numretries = None
        """the physical network to which this Palo Alto firewall belongs to"""
        self.physicalnetworkid = None
        """the private interface of the external firewall"""
        self.privateinterface = None
        """the private security zone of the external firewall"""
        self.privatezone = None
        """name of the provider"""
        self.provider = None
        """the public interface of the external firewall"""
        self.publicinterface = None
        """the public security zone of the external firewall"""
        self.publiczone = None
        """the timeout (in seconds) for requests to the external firewall"""
        self.timeout = None
        """the usage interface of the external firewall"""
        self.usageinterface = None
        """the username that's used to log in to the external firewall"""
        self.username = None
        """the zone ID of the external firewall"""
        self.zoneid = None

