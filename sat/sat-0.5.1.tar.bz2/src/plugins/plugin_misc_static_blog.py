#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for static blogs
# Copyright (C) 2014 Adrien Cossa (souliane@mailoo.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat.core.log import getLogger
log = getLogger(__name__)

from sat.core.i18n import _, D_
from sat.core.constants import Const as C
from sat.core import exceptions
from sat.tools import xml_tools

from twisted.internet import defer
from twisted.words.protocols.jabber import jid


PLUGIN_INFO = {
    "name": "Static Blog Plugin",
    "import_name": "STATIC-BLOG",
    "type": "MISC",
    "protocols": [],
    "dependencies": [],
    "recommendations": ['MISC-ACCOUNT'],  # TODO: remove when all blogs can be retrieved
    "main": "StaticBlog",
    "handler": "no",
    "description": _("""Plugin for static blogs""")
}


class StaticBlog(object):

    params = """
    <params>
    <individual>
    <category name="%(category_name)s" label="%(category_label)s">
        <param name="%(title_name)s" label="%(title_label)s" value="" type="string" security="0"/>
        <param name="%(banner_name)s" label="%(banner_label)s" value="" type="string" security="0"/>
        <param name="%(keywords_name)s" label="%(keywords_label)s" value="" type="string" security="0"/>
        <param name="%(description_name)s" label="%(description_label)s" value="" type="string" security="0"/>
     </category>
    </individual>
    </params>
    """ % {
        'category_name': C.STATIC_BLOG_KEY,
        'category_label': D_(C.STATIC_BLOG_KEY),
        'title_name': C.STATIC_BLOG_PARAM_TITLE,
        'title_label': D_('Page title'),
        'banner_name': C.STATIC_BLOG_PARAM_BANNER,
        'banner_label': D_('Banner URL'),
        'keywords_name': C.STATIC_BLOG_PARAM_KEYWORDS,
        'keywords_label': D_('Keywords'),
        'description_name': C.STATIC_BLOG_PARAM_DESCRIPTION,
        'description_label': D_('Description'),
    }

    def __init__(self, host):
        try:  # TODO: remove this attribute when all blogs can be retrieved
            self.domain = host.plugins['MISC-ACCOUNT'].getNewAccountDomain()
        except KeyError:
            self.domain = None
        host.memory.updateParams(self.params)
        host.importMenu((D_("User"), D_("Public blog")), self._displayPublicBlog, security_limit=1, help_string=D_("Display public blog page"), type_=C.MENU_JID_CONTEXT)

    def _displayPublicBlog(self, menu_data, profile):
        """Check if the blog can be displayed and answer the frontend.

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        @return: dict
        """
        try:
            user_jid = jid.JID(menu_data['jid'])
        except KeyError:
            log.error(_("jid key is not present !"))
            return defer.fail(exceptions.DataError)

        # TODO: remove this check when all blogs can be retrieved
        if self.domain and user_jid.host != self.domain:
            info_ui = xml_tools.XMLUI("popup", title=D_("Not available"))
            info_ui.addText(D_("Retrieving a blog from an external domain is not implemented yet."))
            return {'xmlui': info_ui.toXml()}

        return {"public_blog": user_jid.userhost()}
