import unittest
from decimal import Decimal

from distributed_task.core.serializer import serialize, deserialize


class BasicSerializationTest(unittest.TestCase):

    def test_simple_dict(self):
        simple_dict = {
            'foo': 'bar', 'foo2': {}
        }

        self.assertEqual(simple_dict, deserialize(serialize(simple_dict)), "Dict serialization / deserialization")

    def test_simple_list(self):
        simple_list = [
            ['foo', 'bar'], ['foo2', {}],
        ]

        self.assertEqual(simple_list, deserialize(serialize(simple_list)), "List serialization / deserialization")

    def test_numbers(self):
        numbers = {
            'float': 12.124, 'second': 9.2
        }

        self.assertEqual(numbers, deserialize(serialize(numbers)), "Floats serialization / deserialization")