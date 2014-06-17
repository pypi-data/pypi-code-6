""" Test utility functionality."""
from datetime import datetime
import json
import unittest

from ..utils import JSONSerializable, DatetimeEncoder, \
    json_datetime_hook, FixedOffset


class TestJSONSerializable(unittest.TestCase):

    """ Test JSONSerializable functionality."""

    def setUp(self):
        class A(JSONSerializable):
            @property
            def json(self):
                pass

        self._class = A

    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            JSONSerializable()

        self._class()

    def test_definse_serialize_deserialize(self):
        """ Test classmethods of inherited class."""
        self.assertEqual(self._class.serialize({}), "{}")
        self.assertEqual(self._class.deserialize("{}"), {})

    def test_from_json(self):
        self.assertTrue(isinstance(self._class.from_json('{}'), self._class))

    def test_from_json_incorrect(self):
        with self.assertRaises(ValueError):
            self._class.from_json('[]')


class TestDatetimeEncoderDecoder(unittest.TestCase):

    """ Test DatetimeEncoder and json_datetime_hook functionality."""

    def test_datetime(self):
        obj = datetime.now()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        string = json.dumps(obj, cls=DatetimeEncoder)

        self.assertEqual(obj,
                         json.loads(string, object_hook=json_datetime_hook))

    def test_skip_nondt_obj(self):
        obj = {'__weird__': True}
        string = json.dumps(obj, cls=DatetimeEncoder)
        self.assertEqual(obj,
                         json.loads(string, object_hook=json_datetime_hook))

    def test_datetime_tzinfo(self):
        obj = datetime.now().replace(tzinfo=FixedOffset(3600))

        with self.assertRaises(TypeError):
            json.dumps(obj)

        string = json.dumps(obj, cls=DatetimeEncoder)

        self.assertEqual(obj,
                         json.loads(string, object_hook=json_datetime_hook))
