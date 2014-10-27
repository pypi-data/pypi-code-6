import unittest

from voluptuous import All, Length
from wtforms.validators import ValidationError

from datatypes.core import DictionaryValidator, SingleValueValidator
from datatypes.exceptions import *


class WtfTestDataType(SingleValueValidator):
    def __init__(self):
        super(self.__class__, self).__init__()

    def define_schema(self):
        return All(unicode, Length(max=3))

    def define_error_message(self):
        return "egg"


class TestDictValidator(DictionaryValidator):
    def __init__(self):
        super(self.__class__, self).__init__()

    def define_schema(self):
        return {
            'foo': Length(max=3),
            'bar': Length(max=1)
        }

    def define_error_dictionary(self):
        return {
            'foo': 'sausages'
        }


class TestValidationCore(unittest.TestCase):
    def test_can_filter_none_and_self_from_dictionary(self):
        validator = TestDictValidator()
        dictionary = {u'a': 1, u'b': u'2', u'c': None, u'self': self}
        result = validator.clean_input(dictionary)

        self.assertFalse(None in result.itervalues(),
                         "Result should not contain None: " + repr(result))

        self.assertFalse(u'c' in result.iterkeys(),
                         "Result should not contain key 'c' as this is set to None: " + repr(result))

    def test_can_filter_none_from_nested_dictionary(self):
        validator = TestDictValidator()
        dictionary = {u'a': None, u'b': {u'c': None, u'd': u'd'}}
        result = validator.clean_input(dictionary)

        self.assertFalse(u'a' in result.iterkeys())
        sub_dictionary = result[u'b']
        self.assertFalse(u'c' in sub_dictionary.iterkeys())

    def test_single_value_validator_raises_correct_error_messages(self):
        class TestDatType(SingleValueValidator):
            def __init__(self):
                super(self.__class__, self).__init__()

            def define_schema(self):
                return All(Length(max=3))

            def define_error_message(self):
                return "foo"

        try:
            TestDatType().validate("1234")
            self.fail("Should have throw exception")
        except DataDoesNotMatchSchemaException as exception:
            self.assertEqual(exception.message, "foo")
            self.assertEqual(repr(exception), str(exception))

    def test_dictionary_validator_raises_correct_error_messages(self):
        validator = TestDictValidator()

        try:
            validator.validate({u'foo': u'1234', u'bar': u'12'})
            self.fail("exception should have been thrown")
        except DataDoesNotMatchSchemaException as exception:
            self.assertEqual(exception.field_errors['foo'], 'sausages')
            self.assertEqual(exception.field_errors['bar'], 'length of value must be at most 1')

    def test_raises_error_if_schema_not_defined(self):
        class TestDataType(DictionaryValidator):
            def __init__(self):
                super(self.__class__, self).__init__()

            def define_error_dictionary(self):
                pass

        self.assertRaises(NoSchemaException, TestDataType)

    def test_raises_error_if_error_message_not_defined(self):
        class TestDataType(SingleValueValidator):
            def __init__(self):
                super(self.__class__, self).__init__()

            def define_schema(self):
                pass

        self.assertRaises(ErrorMessageNotDefined, TestDataType)

    def test_raises_error_if_error_dictionary_is_not_defined(self):
        class TestDataType(DictionaryValidator):
            def __init__(self):
                super(self.__class__, self).__init__()

            def define_schema(self):
                pass

        self.assertRaises(NoErrorDictionaryDefined, TestDataType)

    def test_single_value_wtform_error_handling(self):
        validator = WtfTestDataType()

        class FakeField(object):
            data = "1234"

        try:
            wtvalidator = validator.wtform_validator(message="sausages")
            wtvalidator(field=FakeField())
            self.fail("Should have thrown an exception")
        except ValidationError as exception:
            self.assertEqual(exception.message, "sausages")

        try:
            wtvalidator = validator.wtform_validator()
            wtvalidator(field=FakeField())
            self.fail("Should have thrown exception")
        except ValidationError as exception:
            self.assertEqual(exception.message, "egg")

    def test_can_validate_single_field_in_wtf(self):
        class FakeField(object):
            data = u"ab"

        try:
            validator = WtfTestDataType().wtform_validator()
            validator(field=FakeField())
        except ValidationError as exception:
            self.fail("Should not have thrown exception " + repr(exception))
