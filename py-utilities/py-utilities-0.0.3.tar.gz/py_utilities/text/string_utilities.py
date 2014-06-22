#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import array
import random
import string


def random_string(length=16, chars=string.letters+string.digits):
    """
    Returns a random string of size length

    >>> test = random_string()

    >>> len(test)
    16

    """
    return ''.join(random.choice(chars) for x in range(length))


def strip_punctuations(str):
    """
    Returns string stripped of punctuations

    >>> strip_punctuations("asdfs. asdfasdf. asdfsaf? sadfasf!")
    'asdfs asdfasdf asdfsaf sadfasf'

    >>> strip_punctuations("asdfs.....asdfasdf. asdfsaf? sadfasf!")
    'asdfsasdfasdf asdfsaf sadfasf'

    >>> strip_punctuations("")
    ''
    """
    return str.translate(string.maketrans("", ""), string.punctuation)


def ascii_to_str(ascii_list):
    """
    Returns a string from a list of ascii values

    >>> ascii_to_str([104, 101, 108, 108, 111])
    'hello'

    >>> ascii_to_str([82, 121, 97, 110])
    'Ryan'

    """
    return array.array('B', ascii_list).tostring()


def str_to_ascii(str):
    """
    Returns a list of ascii values from a string

    >>> str_to_ascii('hello, world')
    [104, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100]

    >>> str_to_ascii('Ryan')
    [82, 121, 97, 110]

    """
    return array.array('B', str).tolist()


def str_to_bool(str_val):
    """
    Returns True if str_val is in ("yes", "y", "true",  "t", "1"), False if
    str_val is in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]",
    "{}"), and ValueError otherwise.
    """
    if str(str_val).lower() in ("yes", "y", "true",  "t", "1"):
        return True

    if str(str_val).lower() in ("no",  "n", "false", "f", "0", "0.0", "",
                                "none", "[]", "{}"):
        return False

    raise ValueError


def truncate(str, length, trailing_chars='...'):
    """
    Returns a truncated str of length with a trailing '...'

    >>> truncate('foobar', 3)
    'foo...'

    >>> truncate('foobar', 1)
    'f...'

    >>> truncate('', 1)
    ''

    >>> truncate('hello', 100)
    'hello'

    """
    return (str[:length] + trailing_chars) if len(str) > length else str

# vim: filetype=python
