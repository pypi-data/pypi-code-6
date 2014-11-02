# coding: utf-8


class DecimalizeException(Exception):
    pass


class CharsetNotUniqueError(DecimalizeException):
    pass


class DecodeError(DecimalizeException):
    pass
