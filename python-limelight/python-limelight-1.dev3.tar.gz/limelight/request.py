# -*- coding: utf-8 -*-

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# noinspection PyPep8Naming
from socket import timeout as Timeout
from ssl import SSLError

from copy import copy

from voluptuous import Schema

from . import utils
from .mixins import ConversionsMixin, FieldsMixin


class Request(ConversionsMixin, FieldsMixin):
    TIMEOUT = 12
    MAX_TRIES = 3

    def __init__(self, **kwargs):
        self.raw_response = None
        cleaned_data = Schema(self.schema)(kwargs)
        self.__make_request(cleaned_data)

    def __save_response_data(self, data):
        for k, v in data.items():
            setattr(self, utils.to_underscore(k), utils.to_python(v))

    # noinspection PyCallingNonCallable
    def __convert_data(self, data):
        converted_data = {}
        for key, value in data.items():
            conversion_func = getattr(self, "convert__{field}".format(field=key), None)
            if key in self.unconverted_field_labels and conversion_func is None:
                converted_data[key] = value
            elif key in self.unconverted_field_labels and conversion_func is not None:
                converted_data[key] = conversion_func(value)
            elif conversion_func is not None:
                converted_data[utils.to_camel_case(key)] = conversion_func(value)
            else:
                converted_data[utils.to_camel_case(key)] = value
        return converted_data

    def __make_request(self, request_data, tried=0):
        data = copy(request_data)
        data.update({'method': self.__name__,
                     'username': self.username,
                     'password': self.password})
        try:
            request = urlopen(self.endpoint,
                              self.__convert_data(data),
                              timeout=self.TIMEOUT)
            self.raw_response = request.read()
            self.parse_response(self.raw_response)
        except (Timeout, SSLError):
            if tried <= self.MAX_TRIES:
                return self.__make_request(request_data, tried=tried + 1)
            else:
                raise Exception

