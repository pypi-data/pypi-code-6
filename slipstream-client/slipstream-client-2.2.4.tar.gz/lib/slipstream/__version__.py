#!/usr/bin/env python
# coding=latin-1
"""
 SlipStream Client
 =====
 Copyright (C) 2013 SixSq Sarl (sixsq.com)
 =====
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

version = "1.1-0"


def getVersion():
    global version
    return version


def getFullVersion():
    global version
    return "%s" % version


def getCopyright():
    return '''Copyright (c) SixSq S�rl. 2013. http://www.sixsq.com'''


def getLicense():
    return '''
TODO.'''


def getPrettyVersion():
    s = '\nSlipStream Client version: %s\n\n' % getFullVersion()
    s += getCopyright()
    return s


def getLongVersion():
    s = '\nSlipStream Client version: %s\n\n' % getFullVersion()
    s += getCopyright()
    s += getLicense()
    return s
