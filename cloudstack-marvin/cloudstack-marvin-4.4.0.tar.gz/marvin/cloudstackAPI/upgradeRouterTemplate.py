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


"""Upgrades router to use newer template"""
from baseCmd import *
from baseResponse import *
class upgradeRouterTemplateCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """upgrades all routers owned by the specified account"""
        self.account = None
        """upgrades all routers within the specified cluster"""
        self.clusterid = None
        """upgrades all routers owned by the specified domain"""
        self.domainid = None
        """upgrades router with the specified Id"""
        self.id = None
        """upgrades all routers within the specified pod"""
        self.podid = None
        """upgrades all routers within the specified zone"""
        self.zoneid = None
        self.required = []

class upgradeRouterTemplateResponse (baseResponse):
    def __init__(self):
        """the UUID of the latest async job acting on this object"""
        self.jobid = None
        """the current status of the latest async job acting on this object"""
        self.jobstatus = None

