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


"""Adds stratosphere ssp server"""
from baseCmd import *
from baseResponse import *
class addStratosphereSspCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """stratosphere ssp api name"""
        """Required"""
        self.name = None
        """stratosphere ssp server url"""
        """Required"""
        self.url = None
        """the zone ID"""
        """Required"""
        self.zoneid = None
        """stratosphere ssp api password"""
        self.password = None
        """stratosphere ssp tenant uuid"""
        self.tenantuuid = None
        """stratosphere ssp api username"""
        self.username = None
        self.required = ["name","url","zoneid",]

class addStratosphereSspResponse (baseResponse):
    def __init__(self):
        """server id of the stratosphere ssp server"""
        self.hostid = None
        """name"""
        self.name = None
        """url of ssp endpoint"""
        self.url = None
        """zone which this ssp controls"""
        self.zoneid = None

