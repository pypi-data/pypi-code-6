#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011, 2012, 2013, 2014 Jérôme Poisson <goffi@goffi.org>

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

from sat.core.i18n import _
from sat_frontends.tools.strings import addURLToText
from sat.core.log import getLogger
log = getLogger(__name__)

from twisted.internet import defer
from twisted.web import server
from twisted.web.resource import Resource
from twisted.words.protocols.jabber.jid import JID
from datetime import datetime
import uuid
import re
import os

from libervia.server.html_tools import sanitizeHtml
from libervia.server.constants import Const as C


class MicroBlog(Resource):
    isLeaf = True

    ERROR_TEMPLATE = """
                <html>
                <head profile="http://www.w3.org/2005/10/profile">
                    <link rel="icon" type="image/png" href="%(root)ssat_logo_16.png">
                    <title>MICROBLOG ERROR</title>
                </head>
                <body>
                    <h1 style='text-align: center; color: red;'>%(message)s</h1>
                </body>
                </html>
                """

    def __init__(self, host):
        self.host = host
        Resource.__init__(self)
        self.host.bridge.register('entityDataUpdated', self.entityDataUpdatedCb)
        self.host.bridge.register('actionResult', self.actionResultCb)  # FIXME: actionResult is to be removed
        self.avatars_cache = {}
        self.waiting_deferreds = {}

    def entityDataUpdatedCb(self, entity_jid_s, key, value, dummy):
        """Retrieve the avatar we've been waiting for and fires the callback
        for self.getAvatar to return.

        @param entity_jid_s (str): JID of the contact
        @param key (str): entity data key
        @param value (str): entity data value
        @param dummy (str): that would be C.SERVICE_PROFILE
        """
        if key != 'avatar':
            return
        entity_jid_s = entity_jid_s.lower()
        log.debug(_("Received a new avatar for entity %s") % entity_jid_s)
        avatar = C.AVATARS_DIR + value
        self.avatars_cache[entity_jid_s] = avatar
        try:
            self.waiting_deferreds[entity_jid_s][1].callback(avatar)
            del self.waiting_deferreds[entity_jid_s]
        except KeyError:
            pass

    def actionResultCb(self, answer_type, action_id, data, dummy):
        """Fires the callback for self.getAvatar to return

        @param answer_type (str): 'SUPPRESS' or another value that we would ignore
        @param action_id (str): the request ID
        @param data (dict): ignored
        @param dummy (str): that would be C.SERVICE_PROFILE
        """
        # FIXME: actionResult is to be removed. For now we use it to get notified
        # when the requested vCard hasn't been found. Replace with the new system.
        if answer_type != 'SUPPRESS':
            return
        try:
            entity_jid_s = [key for (key, value) in self.waiting_deferreds.items() if value[0] == action_id][0]
        except IndexError:  # impossible to guess the entity
            return
        log.debug(_("Using default avatar for entity %s") % entity_jid_s)
        self.avatars_cache[entity_jid_s] = C.DEFAULT_AVATAR
        self.waiting_deferreds[entity_jid_s][1].callback(C.DEFAULT_AVATAR)
        del self.waiting_deferreds[entity_jid_s]

    def getAvatar(self, profile):
        """Get the avatar of the given profile

        @param profile (str):
        @return: deferred avatar path, relative to the server's root
        """
        jid_s = (profile + '@' + self.host.bridge.getNewAccountDomain()).lower()
        if jid_s in self.avatars_cache:
            return defer.succeed(self.avatars_cache[jid_s])
        # FIXME: request_id is no more need when actionResult is removed
        request_id = self.host.bridge.getCard(jid_s, C.SERVICE_PROFILE)
        self.waiting_deferreds[jid_s] = (request_id, defer.Deferred())
        return self.waiting_deferreds[jid_s][1]

    def render_GET(self, request):
        if not request.postpath:
            return MicroBlog.ERROR_TEMPLATE % {'root': '',
                                               'message': "You must indicate a nickname"}
        else:
            prof_requested = request.postpath[0]
            #TODO: char check: only use alphanumerical chars + some extra(_,-,...) here
            prof_found = self.host.bridge.getProfileName(prof_requested)
            if not prof_found or prof_found == C.SERVICE_PROFILE:
                return MicroBlog.ERROR_TEMPLATE % {'root': '../' * len(request.postpath),
                                                    'message': "Invalid nickname"}
            else:
                def got_jid(pub_jid_s):
                    pub_jid = JID(pub_jid_s)
                    d2 = defer.Deferred()
                    item_id = None
                    try:
                        max_items = int(request.args['max_items'][0])
                    except (ValueError, KeyError):
                        max_items = 10
                    if len(request.postpath) > 1:
                        if request.postpath[1] == 'atom.xml':  # return the atom feed
                            d2.addCallbacks(self.render_atom_feed, self.render_error_blog, [request], None, [request, prof_found], None)
                            self.host.bridge.getLastGroupBlogsAtom(pub_jid.userhost(), max_items, C.SERVICE_PROFILE, d2.callback, d2.errback)
                            return
                        try:  # check if the given path is a valid UUID
                            uuid.UUID(request.postpath[1])
                            item_id = request.postpath[1]
                        except ValueError:
                            pass
                    d2.addCallbacks(self.render_html_blog, self.render_error_blog, [request, prof_found], None, [request, prof_found], None)
                    if item_id:  # display one message and its comments
                        self.host.bridge.getGroupBlogsWithComments(pub_jid.userhost(), [item_id], C.SERVICE_PROFILE, d2.callback, d2.errback)
                    else:  # display the last messages without comment
                        self.host.bridge.getLastGroupBlogs(pub_jid.userhost(), max_items, C.SERVICE_PROFILE, d2.callback, d2.errback)

                d1 = defer.Deferred()
                JID(self.host.bridge.asyncGetParamA('JabberID', 'Connection', 'value', C.SERVER_SECURITY_LIMIT, prof_found, callback=d1.callback, errback=d1.errback))
                d1.addCallbacks(got_jid)

                return server.NOT_DONE_YET

    def render_html_blog(self, mblog_data, request, profile):
        """Retrieve the user parameters before actually rendering the static blog
        @param mblog_data: list of microblog data or list of couple (microblog data, list of microblog data)
        @param request: HTTP request
        @param profile
        """
        d_list = []
        options = {}

        def getCallback(param_name):
            d = defer.Deferred()
            d.addCallback(lambda value: options.update({param_name: value}))
            d_list.append(d)
            return d.callback

        eb = lambda failure: self.render_error_blog(failure, request, profile)

        self.getAvatar(profile).addCallbacks(getCallback('avatar'), eb)
        for param_name in (C.STATIC_BLOG_PARAM_TITLE, C.STATIC_BLOG_PARAM_BANNER, C.STATIC_BLOG_PARAM_KEYWORDS, C.STATIC_BLOG_PARAM_DESCRIPTION):
            self.host.bridge.asyncGetParamA(param_name, C.STATIC_BLOG_KEY, 'value', C.SERVER_SECURITY_LIMIT, profile, callback=getCallback(param_name), errback=eb)

        cb = lambda dummy: self.__render_html_blog(mblog_data, options, request, profile)
        defer.DeferredList(d_list).addCallback(cb)

    def __render_html_blog(self, mblog_data, options, request, profile):
        """Actually render the static blog. If mblog_data is a list of dict, we are missing
        the comments items so we just display the main items. If mblog_data is a list of couple,
        each couple is associating a main item data with the list of its comments, so we render all.
        @param mblog_data: list of microblog data or list of couple (microblog data, list of microblog data)
        @param options: dict defining the blog's parameters
        @param request: the HTTP request
        @profile
        """
        if not isinstance(options, dict):
            options = {}
        user = sanitizeHtml(profile).encode('utf-8')
        root_url = '../' * len(request.postpath)
        base_url = root_url + 'blog/' + user

        def getOption(key):
            return sanitizeHtml(options[key]).encode('utf-8') if key in options else ''

        def getImageOption(key, alt):
            """regexp from http://answers.oreilly.com/topic/280-how-to-validate-urls-with-regular-expressions/"""
            url = options[key].encode('utf-8') if key in options else ''
            regexp = r"^(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[\w-]+)*/[\w-]+\.(gif|png|jpg)$"
            return "<img src='%(url)s' alt='%(alt)s'/>" % {'alt': alt, 'url': url} if re.match(regexp, url) else alt

        request.write("""
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <meta name="keywords" content="%(keywords)s">
                <meta name="description" content="%(description)s">
                <link rel="alternate" type="application/atom+xml" href="%(base)s/atom.xml"/>
                <link rel="stylesheet" type="text/css" href="%(root)scss/blog.css" />
                <link rel="icon" type="image/png" href="%(favicon)s">
                <title>%(title)s</title>
            </head>
            <body>
            <div class="mblog_title"><a href="%(base)s">%(banner_elt)s</a></div>
            """ % {'base': base_url,
                   'root': root_url,
                   'user': user,
                   'keywords': getOption(C.STATIC_BLOG_PARAM_KEYWORDS),
                   'description': getOption(C.STATIC_BLOG_PARAM_DESCRIPTION),
                   'title': getOption(C.STATIC_BLOG_PARAM_TITLE) or "%s's microblog" % user,
                   'favicon': os.path.normpath(root_url + getOption('avatar')),
                   'banner_elt': getImageOption(C.STATIC_BLOG_PARAM_BANNER, getOption(C.STATIC_BLOG_PARAM_TITLE) or user)})
        mblog_data = [(entry if isinstance(entry, tuple) else (entry, [])) for entry in mblog_data]
        mblog_data = sorted(mblog_data, key=lambda entry: (-float(entry[0].get('published', 0))))
        for entry in mblog_data:
            self.__render_html_entry(entry[0], base_url, request)
            comments = sorted(entry[1], key=lambda entry: (float(entry.get('published', 0))))
            for comment in comments:
                self.__render_html_entry(comment, base_url, request)
        request.write('</body></html>')
        request.finish()

    def __render_html_entry(self, entry, base_url, request):
        """Render one microblog entry.
        @param entry: the microblog entry
        @param base_url: the base url of the blog
        @param request: the HTTP request
        """
        timestamp = float(entry.get('published', 0))
        datetime_ = datetime.fromtimestamp(timestamp)
        is_comment = entry['type'] == 'comment'
        if is_comment:
            author = (_("comment from %s") % entry['author']).encode('utf-8')
            item_link = ''
        else:
            author = '&nbsp;'
            item_link = ("%(base)s/%(item_id)s" % {'base': base_url, 'item_id': entry['id']}).encode('utf-8')

        def getText(key):
            if ('%s_xhtml' % key) in entry:
                return entry['%s_xhtml' % key].encode('utf-8')
            elif key in entry:
                processor = addURLToText if key.startswith('content') else sanitizeHtml
                return processor(entry[key]).encode('utf-8')
            return ''

        def addMainItemLink(elem):
            if not item_link or not elem:
                return elem
            return """<a href="%(link)s" class="item_link">%(elem)s</a>""" % {'link': item_link, 'elem': elem}

        header = addMainItemLink("""<div class="mblog_header">
                                      <div class="mblog_metadata">
                                        <div class="mblog_author">%(author)s</div>
                                        <div class="mblog_timestamp">%(date)s</div>
                                      </div>
                                    </div>""" % {'author': author, 'date': datetime_})

        title = addMainItemLink(getText('title'))
        body = getText('content')
        if title:  # insert the title within the body
            body = """<h1>%(title)s</h1>\n%(body)s""" % {'title': title, 'body': body}

        request.write("""<div class="mblog_entry %(extra_style)s">
                           %(header)s
                           <span class="mblog_content">%(content)s</span>
                         </div>""" %
                         {'extra_style': 'mblog_comment' if entry['type'] == 'comment' else '',
                          'item_link': item_link,
                          'header': header,
                          'content': body})

    def render_atom_feed(self, feed, request):
        request.write(feed.encode('utf-8'))
        request.finish()

    def render_error_blog(self, error, request, profile):
        request.write(MicroBlog.ERROR_TEMPLATE % {'root': '../' * len(request.postpath),
                                                  'message': "Can't access requested data"})
        request.finish()
