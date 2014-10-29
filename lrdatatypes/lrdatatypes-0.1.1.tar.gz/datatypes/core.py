from voluptuous import MultipleInvalid, Schema
from wtforms.validators import ValidationError
from collections import OrderedDict

from datatypes.exceptions import *


def filter_none_from_dictionary(dictionary):
    filtered = {}

    for k, v in dictionary.iteritems():
        if isinstance(v, dict):
            filtered[k] = filter_none_from_dictionary(v)
        else:
            if v is not None:
                filtered[k] = v

    return filtered


def alphabetically_sorted_dict(dictionary):
    ordered = OrderedDict()

    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            ordered[k] = alphabetically_sorted_dict(v)
        else:
            ordered[k] = v

    return ordered


class Validator(object):
    def __init__(self, required=False, extra=True):
        self.schema = Schema(schema=self.define_schema(), required=required, extra=extra)

    def clean_input(self, data):
        return data

    def define_schema(self):
        raise NoSchemaException()

    def to_canonical_form(self, data):
        return alphabetically_sorted_dict(self.clean_input(data))

    def validate(self, data):
        raise Exception("You must define a validate method")


class DictionaryValidator(Validator):
    def __init__(self):
        super(DictionaryValidator, self).__init__()
        self.error_dictionary = self.define_error_dictionary()

    def clean_input(self, dictionary):
        return filter_none_from_dictionary(dictionary)

    def validate(self, data):
        try:
            self.schema(self.clean_input(data))
        except MultipleInvalid as exception:
            def translate_voluptuous_errors(voluptuous_exception):
                def flatten_error(error_path):
                    return {error_path: self.error_dictionary.get(error_path, e.error_message)
                            for e in voluptuous_exception.errors if e.path}

                def flatten_path(error):
                    return '.'.join((str(x) for x in error.path if not str(x).isdigit()))

                flattened_errors = {}
                map(lambda e: flattened_errors.update(flatten_error(flatten_path(e))), voluptuous_exception.errors)
                return flattened_errors

            raise DataDoesNotMatchSchemaException(cause=exception,
                                                  value=data,
                                                  field_errors=translate_voluptuous_errors(exception))

    def define_error_dictionary(self):
        raise NoErrorDictionaryDefined()


class SingleValueValidator(Validator):
    class WtfDatatypeValidator(object):
        def __init__(self, validator, message):
            self.validator = validator
            self.message = message

        def __call__(self, form=None, field=None):
            try:
                self.validator.validate(field.data)
            except DataDoesNotMatchSchemaException as e:
                raise ValidationError(self.message if self.message else e.message)

    def __init__(self):
        super(SingleValueValidator, self).__init__()
        self.error_message = self.define_error_message()

    def wtform_validator(self, message=None):
        return SingleValueValidator.WtfDatatypeValidator(self, message)

    def validate(self, data):
        try:
            self.schema(self.clean_input(data))
        except MultipleInvalid as exception:
            raise DataDoesNotMatchSchemaException(cause=exception,
                                                  value=data,
                                                  message=self.error_message,
                                                  field_errors=self.error_message)

    def define_error_message(self):
        raise ErrorMessageNotDefined()


def unicoded(input):
    if isinstance(input, dict):
        return {unicoded(key): unicoded(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicoded(element) for element in input]
    elif isinstance(input, str):
        return input.decode("utf-8") if "decode" in dir(input) else input
    else:
        return input
