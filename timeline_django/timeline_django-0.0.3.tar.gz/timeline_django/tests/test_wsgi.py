# Copyright (c) 2012, Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# GNU Lesser General Public License version 3 (see the file LICENSE).

import threading

from django.dispatch import Signal

from testtools import TestCase
from testtools.matchers import Is

from .. import (
    signals,
    wsgi,
)


class TestWSGI(TestCase):

    def setUp(self):
        super(TestWSGI, self).setUp()
        self.patch(wsgi, '_thread_local', threading.local())

    def test_get_environ_is_None_first_call(self):
        self.assertEqual(None, wsgi.get_environ())

    def test_wsgi_sets_timeline(self):
        environ = {}
        start_response = lambda status, headers: None
        def do_check(environ, start_response):
            self.assertThat(wsgi.get_environ(), Is(environ))
            yield "foo"
        app = wsgi.make_app(do_check)
        out = app(environ, start_response)
        self.assertEqual(["foo"], list(out))

    def test_wsgi_unsets_timeline(self):
        environ = {}
        start_response = lambda status, headers: None
        app = lambda environ, start_response: ["foo"]
        app = wsgi.make_app(app)
        out = app(environ, start_response)
        self.assertEqual(["foo"], list(out))
        self.assertThat(wsgi.get_environ(), Is(None))

    def patch_signal(self, name):
        signal = Signal()
        self.patch(signals, name, signal)
        return signal

    def test_sends_wsgi_request_started_signal(self):
        signal = self.patch_signal('wsgi_request_started')
        called_environs = []
        def capture_signal(sender, environ, signal=None):
            called_environs.append(environ)
        signal.connect(capture_signal)
        wrapped_app = wsgi.make_app(lambda environ, start_response: None)
        environ = object()
        wrapped_app(environ, None)
        self.assertEqual([environ], called_environs)

    def test_sends_wsgi_response_started_signal(self):
        signal = self.patch_signal('wsgi_response_started')
        called_environs = []
        def capture_signal(sender, environ, signal=None):
            called_environs.append(environ)
        signal.connect(capture_signal)
        def app(environ, start_response):
            start_response()
        wrapped_app = wsgi.make_app(app)
        environ = object()
        def start_response(*args, **kwargs):
            pass
        wrapped_app(environ, start_response)
        self.assertEqual([environ], called_environs)

    def test_sends_wsgi_request_started_after_saving_environ(self):
        # Code that listens to the wsgi_request_started signal may
        # want to use the environ, but instead of using the one
        # passed to the signal, they may call get_environ() to get
        # the saved version. That has to be the current request's
        # environ, not any previous request.
        signal = self.patch_signal('wsgi_request_started')
        called_environs = []
        def capture_signal(sender, environ, signal=None):
            # Save the environ that we get from get_environ() at
            # the time of the signal
            called_environs.append(wsgi.get_environ())
        signal.connect(capture_signal)
        wrapped_app = wsgi.make_app(lambda environ, start_response: None)
        environ = object()
        wrapped_app(environ, None)
        # Check that the saved environ matches the one passed to the app
        self.assertEqual([environ], called_environs)


class GeneratorTrackerTests(TestCase):

    def test_consumes_generator(self):
        app = wsgi.generator_tracker(lambda: True, ["foo"])
        self.assertEqual(["foo"], list(app))

    def test_calls_on_finish(self):
        calls = []
        def generator():
            calls.append("consume")
            yield "foo"
        def on_finish():
            calls.append("on_finish")
        app = wsgi.generator_tracker(on_finish, generator())
        self.assertEqual(["foo"], list(app))
        self.assertEqual(["consume", "on_finish"], calls)

    def test_calls_close(self):
        calls = []
        class Body(object):

            def __iter__(self):
                calls.append("consume")
                yield "foo"

            def close(self):
                calls.append("close")

        def on_finish():
            calls.append("on_finish")
        app = wsgi.generator_tracker(on_finish, Body())
        self.assertEqual(["foo"], list(app))
        self.assertEqual(["consume", "close", "on_finish"], calls)
