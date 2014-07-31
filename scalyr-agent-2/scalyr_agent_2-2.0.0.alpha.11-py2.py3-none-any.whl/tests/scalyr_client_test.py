# Copyright 2014, Scalyr, Inc.

import unittest

from scalyr_agent.scalyr_client import AddEventsRequest


class AddEventsRequestTest(unittest.TestCase):

    def setUp(self):
        self.__body = {'token': 'fakeToken'}

    def test_basic_case(self):
        request = AddEventsRequest(self.__body)
        self.assertTrue(request.add_event({'name': 'eventOne'}, timestamp=1L))
        self.assertTrue(request.add_event({'name': 'eventTwo'}, timestamp=2L))

        self.assertEquals(
            request.get_payload(),
            """{"token":"fakeToken", events: [{"name":"eventOne","ts":"1"},{"name":"eventTwo","ts":"2"}]}""")
        request.close()


    def test_multiple_calls_to_get_payload(self):
        request = AddEventsRequest(self.__body)
        self.assertTrue(request.add_event({'name': 'eventOne'}, timestamp=1L))
        self.assertTrue(request.add_event({'name': 'eventTwo'}, timestamp=2L))

        self.assertEquals(request.get_payload(), request.get_payload())
        request.close()

    def test_maximum_bytes_exceeded(self):
        request = AddEventsRequest(self.__body, max_size=70)
        self.assertTrue(request.add_event({'name': 'eventOne'}, timestamp=1L))
        self.assertFalse(request.add_event({'name': 'eventTwo'}, timestamp=2L))

        self.assertEquals(request.get_payload(),
                          """{"token":"fakeToken", events: [{"name":"eventOne","ts":"1"}]}""")
        request.close()

    def test_set_position(self):
        request = AddEventsRequest(self.__body)
        position = request.position()
        self.assertTrue(request.add_event({'name': 'eventOne'}, timestamp=1L))
        self.assertTrue(request.add_event({'name': 'eventTwo'}, timestamp=2L))

        request.set_position(position)
        self.assertTrue(request.add_event({'name': 'eventThree'}, timestamp=3L))

        self.assertEquals(
            request.get_payload(),
            """{"token":"fakeToken", events: [{"name":"eventThree","ts":"3"}]}""")

        request.close()
