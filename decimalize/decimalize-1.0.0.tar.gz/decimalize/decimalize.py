# coding: utf-8

CHARSET = '0123456789abcdefghijklmnopqrstuvwxyz'

from .exceptions import (
    CharsetNotUniqueError,
    DecodeError,
)


class Decimalize(object):
    """decimal encode/decode manager
    """
    def __init__(self, charset=CHARSET):
        self.charset = charset
        self.empty = type(self.charset)()
        self.len = len(charset)
        if self.len != len(set(charset)):
            raise CharsetNotUniqueError(
                'charset_length(%s) != unique_char_length(%s)' % (
                    self.len, len(set(charset))
                )
            )

        self.map = {}
        for i, char in enumerate(charset):
            self.map[char] = i

    def encode(self, number):
        """encode to n-radix.
        """
        string = self.empty
        while number:
            string = self.charset[number % self.len] + string
            number //= self.len
        return string

    def decode(self, string):
        """n-radix decode to decimal.
        """
        strlen = len(string) - 1
        number = 0

        for i, char in enumerate(string):
            try:
                number += self.map[char] * (self.len ** (strlen - i))
            except KeyError:
                raise DecodeError(char)
        return number
