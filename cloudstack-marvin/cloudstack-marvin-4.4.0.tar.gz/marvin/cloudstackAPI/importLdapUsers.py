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


"""Import LDAP users"""
from baseCmd import *
from baseResponse import *
class importLdapUsersCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """Type of the account.  Specify 0 for user, 1 for root admin, and 2 for domain admin"""
        """Required"""
        self.accounttype = None
        """Creates the user under the specified account. If no account is specified, the username will be used as the account name."""
        self.account = None
        """details for account used to store specific parameters"""
        self.accountdetails = []
        """Specifies the domain to which the ldap users are to be imported. If no domain is specified, a domain will created using group parameter. If the group is also not specified, a domain name based on the OU information will be created. If no OU hierarchy exists, will be defaulted to ROOT domain"""
        self.domainid = None
        """Specifies the group name from which the ldap users are to be imported. If no group is specified, all the users will be imported."""
        self.group = None
        """List by keyword"""
        self.keyword = None
        """"""
        self.page = None
        """"""
        self.pagesize = None
        """Specifies a timezone for this command. For more information on the timezone parameter, see Time Zone Format."""
        self.timezone = None
        self.required = ["accounttype",]

class importLdapUsersResponse (baseResponse):
    def __init__(self):
        """The user's domain"""
        self.domain = None
        """The user's email"""
        self.email = None
        """The user's firstname"""
        self.firstname = None
        """The user's lastname"""
        self.lastname = None
        """The user's principle"""
        self.principal = None
        """The user's username"""
        self.username = None

