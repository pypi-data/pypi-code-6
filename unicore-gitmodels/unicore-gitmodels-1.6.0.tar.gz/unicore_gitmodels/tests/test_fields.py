from unittest import TestCase

from unicore_gitmodels.fields import ListField


class TestListField(TestCase):

    def test_none_value(self):
        field = ListField()
        self.assertFalse(field.has_default())

    def test_default_value(self):
        field = ListField(default=[])
        self.assertTrue(field.has_default())

    def test_empty(self):
        self.assertTrue(ListField().empty(None))
        self.assertTrue(ListField().empty([]))
        self.assertFalse(ListField([1]).empty([1]))

    def test_to_python(self):
        self.assertEqual(ListField().to_python([1, 2, 3]), [1, 2, 3])
        self.assertEqual(ListField().to_python("[1, 2, 3]"), [1, 2, 3])

    def test_serialise(self):
        class TestObj(object):
            field = "[1, 2, 3]"
        self.assertEqual(
            ListField(name="field").serialize(TestObj()),
            [1, 2, 3])

    def test_deserialise(self):
        self.assertEqual(
            ListField().deserialize("foo?", "[1, 2, 3]"),
            [1, 2, 3])
