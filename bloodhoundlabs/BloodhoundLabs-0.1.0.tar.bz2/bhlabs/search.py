#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2013 Olemis Lang <olemis at gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


r"""Apache(TM) Bloodhound extensions

Bloodhound search in product context

Copyright 2013 Olemis Lang <olemis at gmail.com>
Licensed under the Apache License
"""

from trac.core import Component, implements
from trac.web.api import IRequestFilter

from bhsearch.web_ui import BloodhoundSearchModule

from multiproduct.env import ProductEnvironment


__all__ = ['ProductSearchModule',]


class ProductSearchModule(Component):
    """Apache(TM) Bloodhound search in product context.
    """
    implements(IRequestFilter)

    @property
    def in_product_ctx(self):
        return isinstance(self.env, ProductEnvironment)

    # IRequestFilter methods
    def pre_process_request(self, req, handler):
        if isinstance(handler, BloodhoundSearchModule) and self.in_product_ctx:
            return BloodhoundSearchModule(self.env.parent)
        return handler

    def post_process_request(self, req, template, data, content_type):
        return template, data, content_type

