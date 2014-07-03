#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


r"""Project dashboard for Apache(TM) Bloodhound

Helper functions and classes.
"""

from functools import update_wrapper
import inspect
from pkg_resources import get_distribution
from urlparse import urlparse
from wsgiref.util import setup_testing_defaults

from trac.core import Component, implements, ExtensionPoint
from trac.util.text import to_unicode
from trac.web.api import Request
from trac.web.chrome import add_link, Chrome
from trac.web.main import RequestDispatcher

#------------------------------------------------------
#    Request handling
#------------------------------------------------------

def dummy_request(env, uname=None):
    environ = {}
    setup_testing_defaults(environ)
    environ.update({
        'REQUEST_METHOD' : 'GET',
        'SCRIPT_NAME' : urlparse(str(env._abs_href())).path,
        'trac.base_url' : str(env._abs_href()),
        })
    req = Request(environ, lambda *args, **kwds: None)
    # Intercept redirection
    req.redirect = lambda *args, **kwds: None
    # Setup user information
    if uname is not None :
        environ['REMOTE_USER'] = req.authname = uname

    rd = RequestDispatcher(env)
    chrome = Chrome(env)
    req.callbacks.update({
        'authname': rd.authenticate,
        'chrome': chrome.prepare_request,
        'hdf': getattr(rd, '_get_hdf', None),
        'lc_time': rd._get_lc_time,
        'locale' : getattr(rd, '_get_locale', None),
        'perm': rd._get_perm,
        'session': rd._get_session,
        'tz': rd._get_timezone,
        'form_token': rd._get_form_token
    })
    return req