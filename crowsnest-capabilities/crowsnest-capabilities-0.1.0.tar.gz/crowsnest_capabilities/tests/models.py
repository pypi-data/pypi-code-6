from decimal import Decimal
from StringIO import StringIO

from mock import patch

from .base import TestCase

from ..exceptions import ValidationError
from ..models import DataField, BaseModel, Action, Event


class DataFieldTestCase(TestCase):

    def test_set_type(self):
        """ Test that setting `type` is validated correclty. """

        name = 'field_name'

        # ensure the given types are valid
        test_types = [None, DataField.STRING, DataField.INT, DataField.NUMBER, DataField.BOOLEAN]
        for test_type in test_types:
            # make sure the constructor and attribute work with valid types
            # also make sure the property is saving the value

            field = DataField(name, type=test_type)
            self.assertIs(field.type, test_type)

            field = DataField(name)
            field.type = test_type
            self.assertIs(field.type, test_type)

        # use some bogus types:
        bogus_types = [
            False,
            0,  # boolean evaluates to False
            1,
            '//asdf',
            DataField(name),  # a complex object
        ]
        for bogus_type in bogus_types:
            # make sure both the constructor and attribute reject the type
            self.assertRaises(AssertionError, DataField, name, type=bogus_type)

            field = DataField(name)
            self.assertRaises(AssertionError, setattr, field, 'type', bogus_type)
            # make sure the value is left unset
            self.assertIsNone(field.type)

    def test_set_valid_values(self):
        """ Test that setting `valid_values` is validated correctly. """

        name = 'field_name'

        # valid_values must be a list or tuple
        test_valid_values = [None, [0, 1, 2], (0, 1, 2)]
        for valid_values in test_valid_values:
            # test the constructor and attr
            field = DataField(name, valid_values=valid_values)
            self.assertIs(field.valid_values, valid_values)

            field = DataField(name)
            field.valid_values = valid_values
            self.assertIs(field.valid_values, valid_values)

        bogus_valid_values = [
            # other iterables
            {0: 0, 1: 1, 2: 2},
            set((0, 1, 2)),
            'asdf',
            False,
            0,  # boolean evaluate to false
            1,
            True,
        ]
        for valid_values in bogus_valid_values:
            # make sure both the constructor and attr reject the type
            self.assertRaises(AssertionError, DataField, name, valid_values=valid_values)
            field = DataField(name)
            self.assertRaises(AssertionError, setattr, field, 'type', valid_values)
            # make sure the value is left unset
            self.assertIsNone(field.valid_values)

    def test_clean_type_string(self):
        """ Test that values are cleaned properly for strings. """
        field = DataField('field_name', type=DataField.STRING)

        # strings pass through
        self.assertEqual(field.clean('asdf'), 'asdf')
        # numbers to strings
        self.assertEqual(field.clean(11), '11')
        self.assertEqual(field.clean(1.1), '1.1')
        # booleans and none to strings
        self.assertEqual(field.clean(True), 'True')
        self.assertEqual(field.clean(False), 'False')
        self.assertEqual(field.clean(None), 'None')

    def test_clean_type_number(self):
        """ Test that values are cleaned properly for numbers. """
        field = DataField('field_name', type=DataField.NUMBER)

        # ints, floats, decimals pass through
        self.assertEqual(field.clean(1), 1)
        self.assertEqual(field.clean(1.1), 1.1)
        self.assertEqual(field.clean(Decimal('1.1')), Decimal('1.1'))

        # valid-looking strings are not coerced
        self.assertRaises(ValidationError, field.clean, '1.1')
        # garbage values are rejected
        self.assertRaises(ValidationError, field.clean, 'asdf')
        # bool is a subclass of int
        # self.assertRaises(ValidationError, field.clean, True)
        # self.assertRaises(ValidationError, field.clean, False)
        self.assertRaises(ValidationError, field.clean, None)

    def test_clean_type_int(self):
        """ Test that values are cleaned properly for integers. """
        field = DataField('field_name', type=DataField.INT)

        # ints passed through
        self.assertEqual(field.clean(1), 1)
        # floats and decimals truncated, but coerce successfully
        self.assertEqual(field.clean(1.1), 1)
        self.assertEqual(field.clean(Decimal('1.1')), 1)
        # valid looking strings coerced
        self.assertEqual(field.clean('1'), 1)
        # booleans coerced
        self.assertEqual(field.clean(False), 0)
        self.assertEqual(field.clean(True), 1)
        # garbage values rejected
        self.assertRaises(ValidationError, field.clean, '1.1')
        self.assertRaises(ValidationError, field.clean, 'asdf')
        self.assertRaises(ValidationError, field.clean, None)

    def test_clean_type_boolean(self):
        """ Test that values are cleaned properly for booleans. """
        field = DataField('field_name', type=DataField.BOOLEAN)

        # true and false passed through
        self.assertIs(field.clean(True), True)
        self.assertIs(field.clean(False), False)
        # coerce everything else
        self.assertIs(field.clean('asdf'), True)
        self.assertIs(field.clean(1), True)
        self.assertIs(field.clean(''), False)
        self.assertIs(field.clean(0), False)
        self.assertIs(field.clean(None), False)

    def test_clean_type_bytes(self):
        field = DataField('field_name', type=DataField.BYTES)

        value = 'asdfjkl;'

        # value passes through as string by default
        self.assertEqual(field.clean(value), value)
        # value is turned into a StringIO with option set to True
        cleaned_value = field.clean(value, create_files_from_bytes=True)
        self.assertTrue(isinstance(cleaned_value, StringIO))
        # make sure read() gives us the original value
        self.assertEqual(cleaned_value.read(), value)

    def test_clean_valid_values(self):
        """ Test that values are cleaned properly for the valid values. """
        field = DataField('field_name', valid_values=[False, 1, 1.11, 'asdf'])

        # matches are allowed through
        self.assertEqual(field.clean(True), True)
        self.assertEqual(field.clean(1), 1)
        self.assertEqual(field.clean(1.11), 1.11)
        self.assertEqual(field.clean('asdf'), 'asdf')

        # types are not coerced
        self.assertRaises(ValidationError, field.clean, None)
        self.assertRaises(ValidationError, field.clean, '1')
        self.assertRaises(ValidationError, field.clean, 1.1)
        self.assertRaises(ValidationError, field.clean, '1.11')
        # exact match required
        self.assertRaises(ValidationError, field.clean, 'asdf ')

    def test_required_true_by_default(self):
        """ Test that fields are required by default """
        field = DataField('field_name')
        self.assertTrue(field.required)


class BaseModelTestCase(TestCase):

    def test_clean_required(self):
        """ Test that required values are handled properly. """
        base = BaseModel()

        fields = [DataField('required', required=True)]
        self.assertEqual(base.clean(fields, {'required': 11}), {'required': 11})
        # missing field causes an error
        self.assertRaises(ValidationError, base.clean, fields, {})

    def test_clean_default(self):
        """ Test that defaults are appropriately supplied for missing fields. """
        base = BaseModel()
        fields = [DataField('default', default=11, required=False)]

        # make sure the default is supplied for us
        self.assertEqual(base.clean(fields, {}), {'default': 11})
        # make sure the default is overridable
        self.assertEqual(base.clean(fields, {'default': 22}), {'default': 22})

    def test_clean_extra_fields(self):
        """ Test that extra, not defined fields are thrown away. """
        base = BaseModel()
        fields = []
        self.assertEqual(base.clean(fields, {'extra': 11}), {})

    def test_clean_data_field_clean(self):
        """ Test that the DataField.clean() is run for supplied values. """
        base = BaseModel()
        field = DataField('field_name')
        with patch.object(field, 'clean') as mock_clean:
            # make sure clean is called with the given value
            base.clean([field], {'field_name': 11})

        mock_clean.assert_called_once_with(11, create_files_from_bytes=False)


class ActionTestCase(TestCase):

    def test_clean_input(self):
        """ Test that clean_input() cleans with the inputs. """
        action = Action('name', {'input': DataField('input')}, {}, 'async_generated_event')
        with patch.object(action, 'clean') as mock_clean:
            action.clean_input({'input': 11})

        mock_clean.assert_called_once_with(action.inputs.values(), {'input': 11}, create_files_from_bytes=False)

    def test_clean_output(self):
        """ Test that clean_output() cleans with the outputs. """
        action = Action('name', {}, {'output': DataField('output')}, 'async_generated_event')
        with patch.object(action, 'clean') as mock_clean:
            action.clean_output({'output': 11})

        mock_clean.assert_called_once_with(action.outputs.values(), {'output': 11}, create_files_from_bytes=False)

    def test_async_generated_event(self):
        """ Test that we look up the related event properly. """
        action = Action('name', {}, {}, 'event.generic.power.changed')
        event = action.async_generated_event
        self.assertTrue(isinstance(event, Event))
        self.assertEqual(event.name, 'event.generic.power.changed')


class EventTestCase(TestCase):

    def test_clean_output(self):
        """ Test that clean_output() cleans with the outputs. """
        event = Event('name', {'output': DataField('output')})
        with patch.object(event, 'clean') as mock_clean:
            event.clean_output({'output': 11})

        mock_clean.assert_called_once_with(event.outputs.values(), {'output': 11}, create_files_from_bytes=False)
