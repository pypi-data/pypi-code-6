from unittest import TestCase

from datatypes.json_serializer import to_json, from_json


class TestJsonSerializer(TestCase):
    def test_can_serialize_and_deserialize_json(self):
        json_dict = {
            "foo": {
                'bar': 'bang'
            }
        }

        self.assertEqual(from_json(to_json(json_dict)), json_dict)