
###############################################################################
#   Copyright 2012 Warren Smith                                               #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
###############################################################################

#######################################################################################################################

class PlainMechanism(object):
    def __init__(self, username="guest", password="guest"):
        self.type = "PLAIN"
        self.username = username
        self.password = password

    def configureStartOk(self, start_ok):
        start_ok.mechanism = self.type
        start_ok.response = "\0" + self.username + "\0" + self.password

#######################################################################################################################

class X509Mechanism(object):
    def __init__(self):
        self.type = "EXTERNAL"

    def configureStartOk(self, start_ok):
        start_ok.mechanism = self.type
        start_ok.response = "\0\0"

#######################################################################################################################
