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


"""Lists all available OS mappings for given hypervisor"""
from baseCmd import *
from baseResponse import *
class listGuestOsMappingCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """list Guest OS mapping by hypervisor"""
        self.hypervisor = None
        """list Guest OS mapping by hypervisor version. Must be used with hypervisor parameter"""
        self.hypervisorversion = None
        """list mapping by its UUID"""
        self.id = None
        """List by keyword"""
        self.keyword = None
        """list mapping by Guest OS Type UUID"""
        self.ostypeid = None
        """"""
        self.page = None
        """"""
        self.pagesize = None
        self.required = []

class listGuestOsMappingResponse (baseResponse):
    def __init__(self):
        """the ID of the Guest OS mapping"""
        self.id = None
        """the hypervisor"""
        self.hypervisor = None
        """version of the hypervisor for mapping"""
        self.hypervisorversion = None
        """is the mapping user defined"""
        self.isuserdefined = None
        """standard display name for the Guest OS"""
        self.osdisplayname = None
        """hypervisor specific name for the Guest OS"""
        self.osnameforhypervisor = None
        """the ID of the Guest OS type"""
        self.ostypeid = None

