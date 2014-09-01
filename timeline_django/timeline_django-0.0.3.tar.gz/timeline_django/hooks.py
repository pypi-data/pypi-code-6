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

from datetime import timedelta

import django.core.signals
import django.db.backends.signals

from . import signals


class TimelineReceiver(object):
    """Converts django signals in to `Timeline` entries.

    To use this instantiate on instance, passing a callable that
    will return the timeline, and then call `connect_to_signals`.
    """

    REQUEST_START_CATEGORY = "request-start"
    REQUEST_STOP_CATEGORY = "request-stop"
    REQUEST_EXCEPTION_CATEGORY = "request-exception"
    CONNECTION_CREATED_CATEGORY = "connection-created"
    WSGI_REQUEST_CATEGORY = "wsgi_request-start"
    WSGI_RESPONSE_CATEGORY = "wsgi_response-start"

    def __init__(self, timeline_factory):
        """Create a TimelineReceiver.

        :param timeline_factory: a callable that takes no arguments,
            and returns a `Timeline` object or `None`. This will
            be called each time a `Timeline` is needed in reponse
            to a signal.
        """
        self.timeline_factory = timeline_factory

    def _model_name(self, model_cls):
        if model_cls is None:
            return "None"
        return "%s.%s" % (model_cls.__module__, model_cls.__name__)

    def request_started(self, sender, **kwargs):
        self._do_instantaneous_action(self.REQUEST_START_CATEGORY, self._model_name(sender))

    def request_finished(self, sender, **kwargs):
        self._do_instantaneous_action(self.REQUEST_STOP_CATEGORY, self._model_name(sender))

    def _do_instantaneous_action(self, category, detail):
        timeline = self.timeline_factory()
        if timeline is None:
            return
        action = timeline.start(category, detail)
        action.duration = timedelta()

    def got_request_exception(self, sender, **kwargs):
        self._do_instantaneous_action(self.REQUEST_EXCEPTION_CATEGORY,
                self._model_name(sender))

    def connection_created(self, sender, **kwargs):
        connection = kwargs.get('connection', None)
        if connection is not None:
            connection_name = connection.alias
        else:
            connection_name = "(unknown)"
        self._do_instantaneous_action(self.CONNECTION_CREATED_CATEGORY,
                connection_name)

    def wsgi_request_started(self, sender, **kwargs):
        self._do_instantaneous_action(self.WSGI_REQUEST_CATEGORY,
                self._model_name(sender))

    def wsgi_response_started(self, sender, **kwargs):
        self._do_instantaneous_action(self.WSGI_RESPONSE_CATEGORY,
                self._model_name(sender))

    def connect_to_signals(self):
        """Connect the callbacks to their corresponding signals."""
        django.core.signals.request_started.connect(
            self.request_started, weak=False, dispatch_uid="timeline_django")
        django.core.signals.request_finished.connect(
            self.request_finished, weak=False, dispatch_uid="timeline_django")
        django.core.signals.got_request_exception.connect(
            self.got_request_exception, weak=False, dispatch_uid="timeline_django")
        django.db.backends.signals.connection_created.connect(
            self.connection_created, weak=False, dispatch_uid="timeline_django")
        signals.wsgi_request_started.connect(
            self.wsgi_request_started, weak=False, dispatch_uid="timeline_django")
        signals.wsgi_response_started.connect(
            self.wsgi_response_started, weak=False, dispatch_uid="timeline_django")
