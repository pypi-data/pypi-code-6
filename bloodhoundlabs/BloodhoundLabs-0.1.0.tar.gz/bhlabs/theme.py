
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

import copy
import sys

import pkg_resources

from trac.core import implements
from trac.web.api import IRequestFilter, ITemplateStreamFilter
from trac.web.chrome import INavigationContributor, ITemplateProvider

from themeengine.api import IThemeProvider

from bhtheme.theme import BloodhoundTheme

class BloodhoundLabsTheme(BloodhoundTheme):
    """Advanced Bloodhound theme
    """

    implements(IRequestFilter, INavigationContributor, ITemplateProvider,
               ITemplateStreamFilter)

    BLOODHOUND_TEMPLATE_MAP = copy.deepcopy(BloodhoundTheme.BLOODHOUND_TEMPLATE_MAP)

    BLOODHOUND_TEMPLATE_MAP.update({
            'attachment.html' : ('bh_fu_attachment.html', None),
            'attach_file_form.html' : ('bh_fu_attach_file_form.html', None),
            'list_of_attachments.html' : ('bh_fu_list_of_attachments.html', None),
            'ticket.html': ('bh_fu_ticket.html', None),
            'milestone_view.html': ('bh_fu_milestone_view.html', None),
            'wiki_view.html' : ('bh_fu_wiki_view.html',None)
            ,})

    # IThemeProvider methods

    def get_theme_info(self, name):
        """Reuse Bloodhound theme's info and tweak when necessary
        """
        info = super(BloodhoundLabsTheme, self).get_theme_info('Bloodhound')
        info.update(template=pkg_resources.resource_filename('bhtheme', 
                                                             info['template']),
                    htdocs=pkg_resources.resource_filename('bhtheme', 'htdocs'))
        return info

    def get_template_overrides(name):
        return []

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        """BloodhoundLabs htdocs
        """
        yield 'bhlabs', pkg_resources.resource_filename(__name__, 'htdocs')

    def get_templates_dirs(self):
        """BloodhoundLabs templates
        """
        yield pkg_resources.resource_filename(__name__, 'templates')

