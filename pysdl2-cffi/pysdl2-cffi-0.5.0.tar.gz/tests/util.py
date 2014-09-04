# Utilities to deal with Python 3
# Daniel Holth <dholth@fastmail.fm>

import string

import re

class Formatter(string.Formatter):
    """
    Custom formatter with utf-8 conversion.
    """

    # USELESS BS DUE TO ''.format() MISMATCH

    def convert_field(self, value, conversion):
        if conversion == 'u':
            return value.decode('utf-8', 'replace')
        return string.Formatter.convert_field(self, value, conversion)

class ustr(object):
    def __init__(self, text):
        self.text = text

    def __mod__(self, other):
        if not isinstance(other, (list, tuple)):
            other = (other,)

        # every other value is a %x
        values = iter(re.split('(%[^%])', self.text))
        subs = iter(other)

        def process():
            while True:
                yield next(values)
                format = next(values)
                if format == '%U':
                    yield next(subs).decode('utf-8', 'replace')
                else:
                    yield format % (next(subs),)

        return ''.join(process())

