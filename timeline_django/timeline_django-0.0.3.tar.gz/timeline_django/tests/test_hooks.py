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
from django.dispatch import Signal
from testtools import TestCase
from timeline import Timeline

from .. import signals
from ..hooks import TimelineReceiver


class TestModel(object):

    # Must be the FQPN of the class to correspond with
    # TimelineReceiver._model_name
    NAME = '%s.%s' % (__name__, 'TestModel')


class TestConnection(object):

    def __init__(self, alias=None):
        if alias is None:
            alias = "foo"
        self.alias = alias


class TimelineReceiverTests(TestCase):

    def get_timeline_receiver(self):
        timeline = Timeline()
        return TimelineReceiver(lambda: timeline), timeline

    def test_model_name(self):
        receiver = TimelineReceiver(lambda: None)
        self.assertEqual(TestModel.NAME, receiver._model_name(TestModel))

    def test_model_name_when_None(self):
        receiver = TimelineReceiver(lambda: None)
        self.assertEqual('None', receiver._model_name(None))

    def test_request_started_with_no_timeline(self):
        receiver = TimelineReceiver(lambda: None)
        # Mustn't crash due to trying to use a None timeline
        receiver.request_started(TestModel)
        # And must be able to complete the request
        receiver.request_finished(TestModel)

    def test_request_started_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        self.assertEqual(1, len(timeline.actions))

    def test_request_started_sets_request_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        # -start is appended as this is a nestable action
        self.assertEqual('request-start', timeline.actions[0].category)

    def test_request_started_sets_sender_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        self.assertEqual(TestModel.NAME, timeline.actions[0].detail)

    def test_request_started_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        # If this passes it means the action was completed as an
        # instantaneous action. This is so nesting can be done,
        # as the action may well trigger SQL
        self.assertEqual(timedelta(), timeline.actions[0].duration)

    def test_request_finished_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        receiver.request_finished(TestModel)
        self.assertEqual(2, len(timeline.actions))

    def test_request_finished_sets_request_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        receiver.request_finished(TestModel)
        # -finish is appended as this is a nestable action
        self.assertEqual('request-stop', timeline.actions[-1].category)

    def test_request_finished_sets_model_name_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        receiver.request_finished(TestModel)
        self.assertEqual(TestModel.NAME, timeline.actions[-1].detail)

    def test_request_finished_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        receiver.request_finished(TestModel)
        self.assertEqual(timedelta(), timeline.actions[-1].duration)

    def test_nested_request(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.request_started(TestModel)
        receiver.request_started(TestModel)
        receiver.request_finished(TestModel)
        receiver.request_finished(TestModel)
        self.assertEqual(4, len(timeline.actions))

    def test_got_request_exception_with_no_timeline(self):
        receiver = TimelineReceiver(lambda: None)
        # Mustn't crash due to trying to use a None timeline
        receiver.got_request_exception(TestModel)

    def test_got_request_exception_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.got_request_exception(TestModel)
        self.assertEqual(1, len(timeline.actions))

    def test_got_request_exception_sets_request_exception_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.got_request_exception(TestModel)
        self.assertEqual('request-exception', timeline.actions[0].category)

    def test_got_request_exception_sets_sender_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.got_request_exception(TestModel)
        self.assertEqual(TestModel.NAME, timeline.actions[0].detail)

    def test_got_request_exception_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.got_request_exception(TestModel)
        self.assertEqual(timedelta(), timeline.actions[0].duration)

    def test_wsgi_request_started_with_no_timeline(self):
        receiver = TimelineReceiver(lambda: None)
        # Mustn't crash due to trying to use a None timeline
        receiver.wsgi_request_started(TestModel)

    def test_wsgi_request_started_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_request_started(TestModel)
        self.assertEqual(1, len(timeline.actions))

    def test_wsgi_request_started_sets_wsgi_request_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_request_started(TestModel)
        # -start is appended as this is a nestable action
        self.assertEqual('wsgi_request-start', timeline.actions[0].category)

    def test_wsgi_request_started_sets_sender_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_request_started(TestModel)
        self.assertEqual(TestModel.NAME, timeline.actions[0].detail)

    def test_wsgi_request_started_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_request_started(TestModel)
        # If this passes it means the action was completed as an
        # instantaneous action. This is so nesting can be done,
        # as the action may well trigger SQL
        self.assertEqual(timedelta(), timeline.actions[0].duration)

    def test_wsgi_response_started_with_no_timeline(self):
        receiver = TimelineReceiver(lambda: None)
        # Mustn't crash due to trying to use a None timeline
        receiver.wsgi_response_started(TestModel)

    def test_wsgi_response_started_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_response_started(TestModel)
        self.assertEqual(1, len(timeline.actions))

    def test_wsgi_response_started_sets_wsgi_response_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_response_started(TestModel)
        # -start is appended as this is a nestable action
        self.assertEqual('wsgi_response-start', timeline.actions[0].category)

    def test_wsgi_response_started_sets_sender_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_response_started(TestModel)
        self.assertEqual(TestModel.NAME, timeline.actions[0].detail)

    def test_wsgi_response_started_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.wsgi_response_started(TestModel)
        # If this passes it means the action was completed as an
        # instantaneous action. This is so nesting can be done,
        # as the action may well trigger SQL
        self.assertEqual(timedelta(), timeline.actions[0].duration)

    def test_connection_created_with_no_timeline(self):
        receiver = TimelineReceiver(lambda: None)
        connection = TestConnection()
        # Mustn't crash due to trying to use a None timeline
        receiver.connection_created(TestModel, connection=connection)

    def test_connection_created_adds_action(self):
        receiver, timeline = self.get_timeline_receiver()
        connection = TestConnection()
        receiver.connection_created(TestModel, connection=connection)
        self.assertEqual(1, len(timeline.actions))

    def test_connection_created_sets_connection_created_as_category(self):
        receiver, timeline = self.get_timeline_receiver()
        connection = TestConnection()
        receiver.connection_created(TestModel, connection=connection)
        self.assertEqual('connection-created', timeline.actions[0].category)

    def test_connection_created_sets_connection_name_as_detail(self):
        receiver, timeline = self.get_timeline_receiver()
        connection_name = self.getUniqueString()
        connection = TestConnection(alias=connection_name)
        receiver.connection_created(TestModel, connection=connection)
        self.assertEqual(connection_name, timeline.actions[0].detail)

    def test_connection_created_sets_unknown_if_connection_missing(self):
        receiver, timeline = self.get_timeline_receiver()
        receiver.connection_created(TestModel)
        self.assertEqual("(unknown)", timeline.actions[0].detail)

    def test_connection_created_finishes_action(self):
        receiver, timeline = self.get_timeline_receiver()
        connection = TestConnection()
        receiver.connection_created(TestModel, connection=connection)
        self.assertEqual(timedelta(), timeline.actions[0].duration)

    def patch_signal(self, module, signal_name):
        signal = Signal()
        self.patch(module, signal_name, signal)
        return signal

    def register_signal(self, module, signal_name):
        signal = self.patch_signal(module, signal_name)
        receiver, timeline = self.get_timeline_receiver()
        receiver.connect_to_signals()
        return signal, receiver

    def test_register_signals_registers_request_started(self):
        signal, receiver = self.register_signal(django.core.signals, 'request_started')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.request_started, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])

    def test_register_signals_registers_request_finished(self):
        signal, receiver = self.register_signal(django.core.signals, 'request_finished')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.request_finished, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])

    def test_register_signals_registers_got_request_exception(self):
        signal, receiver = self.register_signal(django.core.signals, 'got_request_exception')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.got_request_exception, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])

    def test_register_signals_registers_connection_created(self):
        signal, receiver = self.register_signal(django.db.backends.signals, 'connection_created')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.connection_created, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])

    def test_register_signals_registers_wsgi_request_started(self):
        signal, receiver = self.register_signal(signals, 'wsgi_request_started')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.wsgi_request_started, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])

    def test_register_signals_registers_wsgi_response_started(self):
        signal, receiver = self.register_signal(signals, 'wsgi_response_started')
        self.assertEqual(1, len(signal.receivers))
        self.assertEqual(receiver.wsgi_response_started, signal.receivers[0][1])
        self.assertEqual("timeline_django", signal.receivers[0][0][0])
