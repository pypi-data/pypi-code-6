#coding:utf8

"""
Created on 2014-10-14

@author: tufei
@description:
         
Copyright (c) 2013 infohold inc. All rights reserved.
"""
import dhkit.validators


class ArgumentError(Exception):
    """参数异常
    """


class Field(object):
    default_validators = []

    def __init__(self, name, required=True, default=None):
        self.name = name
        self.validators = [] + self.default_validators
        self.required = required
        self.default = default

    def validate(self, value):
        if value in dhkit.validators.EMPTY_VALUES:
            if self.required:
                raise ArgumentError("Argument:[%s] can not be empty." % self.name)
            elif self.default is not None:
                value = self.default
            else:
                return value
        try:
            cleaned_value = self.to_python(value)
            for _validator in self.validators:
                _validator(cleaned_value)
            return cleaned_value
        except dhkit.validators.ValidationError, e:
            raise ArgumentError("Argument:[%s] Invalid. error message: %s" % (self.name, e.message))

    def to_python(self, value):
        return value


class StringField(Field):

    def __init__(self, name, required=True, default=None, min_length=None, max_length=None):
        super(StringField, self).__init__(name, required, default)
        self.max_length = max_length
        self.min_length = min_length
        if self.max_length:
            self.validators.append(dhkit.validators.MaxLengthValidator(int(self.max_length)))
        if self.min_length:
            self.validators.append(dhkit.validators.MinLengthValidator(int(self.min_length)))

    def to_python(self, value):
        return str(value)


class IntegerField(Field):

    def __init__(self, name, required=True, default=None, min_value=None, max_value=None):
        super(IntegerField, self).__init__(name, required, default)
        self.max_value = max_value
        self.min_value = min_value
        if self.max_value:
            self.validators.append(dhkit.validators.MaxValueValidator(int(self.max_value)))
        if self.min_value:
            self.validators.append(dhkit.validators.MinValueValidator(int(self.min_value)))

    def to_python(self, value):
        try:
            return int(value)
        except ValueError:
            raise ArgumentError("Argument:[%s] invalid" % self.name)


class DateField(StringField):

    def __init__(self, name, required=True, default=None):
        super(DateField, self).__init__(name, required, default)
        self.validators.append(dhkit.validators.DateValidator())


class PhoneField(StringField):

    def __init__(self, name, required=True, default=None):
        super(PhoneField, self).__init__(name, required, default)
        self.validators.append(dhkit.validators.PhoneValidator())


class EmailField(StringField):

    def __init__(self, name, required=True, default=None):
        super(EmailField, self).__init__(name, required, default)
        self.validators.append(dhkit.validators.EmailValidator())


class AcceptField(Field):

    def __init__(self, name, accept_values, required=True, default=None):
        super(AcceptField, self).__init__(name, required, default)
        self.validators.append(dhkit.validators.AcceptValidator(accept_values))


class BooleanField(AcceptField):

    def __init__(self, name, required=True, default=None):
        accept_values = ("false", "False", "FALSE", False, "true", "True", "TRUE", True)
        super(BooleanField, self).__init__(name, accept_values, required, default)

    def to_python(self, value):
        return False if str(value).lower() == "false" else True


def validator(filed_cls, **kwargs):
    return filed_cls(**kwargs)