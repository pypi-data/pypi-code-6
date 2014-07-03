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

import re

from trac.web.chrome import add_stylesheet, add_script
from trac.core import Component, implements, TracError
from trac.web.api import IRequestHandler

from bhdashboard.api import ILayoutProvider

class JqueryUILayout(Component):
    """Implement some basic jquery UI layouts
    """
    implements(ILayoutProvider, IRequestHandler)

    # ILayoutProvider methods
    def get_layouts(self):
        """Supported layouts.
        """
        yield 'jquerylayout'

    def get_layout_description(self, name):
        return {
                'jquerylayout': "Jquery UI Layout"
            }[name]

    def expand_layout(self, name, context, options):
        """Specify jquery layout template
        """
        req = context.req
        add_stylesheet(req, 'dashboard/css/bootstrap.css')
        add_stylesheet(req, 'dashboard/css/bootstrap-responsive.css')
        add_stylesheet(req, 'bhlabs/css/layout-default.css')
        add_stylesheet(req, 'bhlabs/jquery/css/base/jquery.ui.all.css')
        add_script(req, 'bhlabs/jquery/js/jquery-ui.js')
        add_script(req, 'bhlabs/jquery/js/jquery.layout.js')

        return {'template': 'jq_layout.html'}

    # IRequestHandler methods

    RE_MATCH = re.compile(r'^/jq_layout/(\d+)$')

    def match_request(self, req):
        m = self.RE_MATCH.match(req.path_info)
        if m:
            req.jq_layout_ticket = m.group(1)
            return True

    def process_request(self, req):
        return 'jq_layout_view.html', {'ticket_id' : req.jq_layout_ticket}, None