from decimal import Decimal
from StringIO import StringIO

from .exceptions import ValidationError
from .structure import capabilities


class DataField(object):

    STRING = '//str'
    NUMBER = '//num'
    INT = '//int'
    BOOLEAN = '//bool'
    BYTES = '//bytes'

    def __init__(self, name, type=None, valid_values=None, required=True, default=None):
        self.name = name

        self.type = type
        self.valid_values = valid_values
        self.required = required
        self.default = default

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        # make sure the value is a valid type, if set
        if value is not None:
            assert value in [self.STRING, self.NUMBER, self.INT, self.BOOLEAN, self.BYTES], self.name + "'s type is not valid"
        self._type = value

    @property
    def valid_values(self):
        return self._valid_values

    @valid_values.setter
    def valid_values(self, value):
        # make sure valid_values is a list or tuple, if set
        if value is not None:
            assert isinstance(value, list) or isinstance(value, tuple), self.name + "'s valid_values is not a list"
        self._valid_values = value

    def clean(self, value, create_files_from_bytes=False):
        """ Using our rules, clean a value """
        # if a type is required, make sure it is valid
        if self.type:
            if self.type == self.STRING:
                # coerce to a string
                value = str(value)
            elif self.type == self.NUMBER:
                # make sure it's an int, float, or Decimal
                if not any((isinstance(value, int), isinstance(value, float), isinstance(value, Decimal))):
                    raise ValidationError('`{}` must be a number'.format(self.name))
            elif self.type == self.INT:
                # try to coerce to an int
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    raise ValidationError('`{}` must be an int'.format(self.name))
            elif self.type == self.BOOLEAN:
                # coerce to a bool
                # no error handling, because anything is forceable to a bool
                value = bool(value)
            elif self.type == self.BYTES:
                if create_files_from_bytes:
                    # make it a StringIO
                    value = StringIO(value)
                else:
                    # otherwise, just keep it a string
                    value = str(value)


        # if valid values are defined, make sure it is one of them
        if self.valid_values:
            if not value in self.valid_values:
                raise ValidationError('`{}` must be one of {}'.format(self.name, self.valid_values))

        return value


class BaseModel(object):
    """ base that can clean based on fields """
    def clean(self, fields, data, create_files_from_bytes=False):
        """ Cleans the data with the supplied list of fields """
        cleaned_data = {}

        # use our fields to build a clean data set
        for field in fields:
            # if a value is missing
            if field.name not in data:
                # if required, raise a ValidationError
                if field.required:
                    raise ValidationError('`{}` is required'.format(field.name))
                # otherwise, supply the default
                cleaned_data[field.name] = field.default
            # clean the given value
            else:
                cleaned_data[field.name] = field.clean(data[field.name], create_files_from_bytes=create_files_from_bytes)

        return cleaned_data

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class Action(BaseModel):
    def __init__(self, name, inputs, outputs, async_generated_event_name):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.async_generated_event_name = async_generated_event_name

    def clean_input(self, data, create_files_from_bytes=False):
        """ Takes some data and cleans it using inputs """
        return self.clean(self.inputs.values(), data, create_files_from_bytes=create_files_from_bytes)

    def clean_output(self, data, create_files_from_bytes=False):
        """ Takes some data and cleans it using outputs """
        return self.clean(self.outputs.values(), data, create_files_from_bytes=create_files_from_bytes)

    @property
    def async_generated_event(self):
        """ Look up the event instance self.async_generated_event_name refers to """
        return capabilities[self.async_generated_event_name]


class Event(BaseModel):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    def clean_output(self, data, create_files_from_bytes=False):
        """ Takes some data and cleans it using outputs """
        return self.clean(self.outputs.values(), data, create_files_from_bytes=create_files_from_bytes)
