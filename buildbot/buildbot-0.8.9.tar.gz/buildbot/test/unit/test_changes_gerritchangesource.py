# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc[''], 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

import types

from buildbot.changes import gerritchangesource
from buildbot.test.util import changesource
from buildbot.util import json
from twisted.trial import unittest


class TestGerritChangeSource(changesource.ChangeSourceMixin,
                             unittest.TestCase):

    def setUp(self):
        return self.setUpChangeSource()

    def tearDown(self):
        return self.tearDownChangeSource()

    def newChangeSource(self, host, user, *args, **kwargs):
        s = gerritchangesource.GerritChangeSource(
            host, user, *args, **kwargs)
        self.attachChangeSource(s)
        return s

    # tests

    def test_describe(self):
        s = self.newChangeSource('somehost', 'someuser')
        self.assertSubstring("GerritChangeSource", s.describe())

    # TODO: test the backoff algorithm

    # this variable is reused in test_steps_source_repo
    # to ensure correct integration between change source and repo step
    expected_change = {'category': u'patchset-created',
                       'files': ['unknown'],
                       'repository': u'ssh://someuser@somehost:29418/pr',
                       'author': u'Dustin <dustin@mozilla.com>',
                       'comments': u'fix 1234',
                       'project': u'pr',
                       'branch': u'br/4321',
                       'revlink': u'http://buildbot.net',
                       'properties': {u'event.change.owner.email': u'dustin@mozilla.com',
                                      u'event.change.subject': u'fix 1234',
                                      u'event.change.project': u'pr',
                                      u'event.change.owner.name': u'Dustin',
                                      u'event.change.number': u'4321',
                                      u'event.change.url': u'http://buildbot.net',
                                      u'event.change.branch': u'br',
                                      u'event.type': u'patchset-created',
                                      u'event.patchSet.revision': u'abcdef',
                                      u'event.patchSet.number': u'12'},
                       u'revision': u'abcdef'}

    def test_lineReceived_patchset_created(self):
        s = self.newChangeSource('somehost', 'someuser')
        d = s.lineReceived(json.dumps(dict(
            type="patchset-created",
            change=dict(
                branch="br",
                project="pr",
                number="4321",
                owner=dict(name="Dustin", email="dustin@mozilla.com"),
                url="http://buildbot.net",
                subject="fix 1234"
            ),
            patchSet=dict(revision="abcdef", number="12")
        )))

        def check(_):
            self.failUnlessEqual(len(self.changes_added), 1)
            c = self.changes_added[0]
            for k, v in c.items():
                self.assertEqual(self.expected_change[k], v)
        d.addCallback(check)
        return d

    change_merged_event = {
        "type": "change-merged",
        "change": {
            "branch": "br",
            "project": "pr",
            "number": "4321",
            "owner": {"name": "Chuck", "email": "chuck@norris.com"},
            "url": "http://buildbot.net",
            "subject": "fix 1234"},
        "patchSet": {"revision": "abcdefj", "number": "13"}
    }

    def test_handled_events_filter_true(self):
        s = self.newChangeSource(
            'somehost', 'some_choosy_user', handled_events=["change-merged"])
        d = s.lineReceived(json.dumps(self.change_merged_event))

        def check(_):
            self.failUnlessEqual(len(self.changes_added), 1)
            c = self.changes_added[0]
            self.failUnlessEqual(c["category"], "change-merged")
        d.addCallback(check)
        return d

    def test_handled_events_filter_false(self):
        s = self.newChangeSource(
            'somehost', 'some_choosy_user')
        d = s.lineReceived(json.dumps(self.change_merged_event))
        check = lambda _: self.failUnlessEqual(len(self.changes_added), 0)
        d.addCallback(check)
        return d

    def test_custom_handler(self):
        s = self.newChangeSource(
            'somehost', 'some_choosy_user',
            handled_events=["change-merged"])

        def custom_handler(self, properties, event):
            event['change']['project'] = "world"
            return self.addChangeFromEvent(properties, event)
        # Patches class to not bother with the inheritance
        s.eventReceived_change_merged = types.MethodType(custom_handler, s)
        d = s.lineReceived(json.dumps(self.change_merged_event))

        def check(_):
            self.failUnlessEqual(len(self.changes_added), 1)
            c = self.changes_added[0]
            self.failUnlessEqual(c['project'], "world")
        d.addCallback(check)
        return d
