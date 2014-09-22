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


"""Updates an existing autoscale vm profile."""
from baseCmd import *
from baseResponse import *
class updateAutoScaleVmProfileCmd (baseCmd):
    def __init__(self):
        self.isAsync = "true"
        """the ID of the autoscale vm profile"""
        """Required"""
        self.id = None
        """the ID of the user used to launch and destroy the VMs"""
        self.autoscaleuserid = None
        """counterparam list. Example: counterparam[0].name=snmpcommunity&counterparam[0].value=public&counterparam[1].name=snmpport&counterparam[1].value=161"""
        self.counterparam = []
        """an optional field, in case you want to set a custom id to the resource. Allowed to Root Admins only"""
        self.customid = None
        """the time allowed for existing connections to get closed before a vm is destroyed"""
        self.destroyvmgraceperiod = None
        """an optional field, whether to the display the profile to the end user or not"""
        self.fordisplay = None
        """the template of the auto deployed virtual machine"""
        self.templateid = None
        self.required = ["id",]

class updateAutoScaleVmProfileResponse (baseResponse):
    def __init__(self):
        """the autoscale vm profile ID"""
        self.id = None
        """the account owning the instance group"""
        self.account = None
        """the ID of the user used to launch and destroy the VMs"""
        self.autoscaleuserid = None
        """the time allowed for existing connections to get closed before a vm is destroyed"""
        self.destroyvmgraceperiod = None
        """the domain name of the vm profile"""
        self.domain = None
        """the domain ID of the vm profile"""
        self.domainid = None
        """is profile for display to the regular user"""
        self.fordisplay = None
        """parameters other than zoneId/serviceOfferringId/templateId to be used while deploying a virtual machine"""
        self.otherdeployparams = None
        """the project name of the vm profile"""
        self.project = None
        """the project id vm profile"""
        self.projectid = None
        """the service offering to be used while deploying a virtual machine"""
        self.serviceofferingid = None
        """the template to be used while deploying a virtual machine"""
        self.templateid = None
        """the availability zone to be used while deploying a virtual machine"""
        self.zoneid = None

