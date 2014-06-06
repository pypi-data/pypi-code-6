#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'


def simple_encode(word):
    """Given two bytes interpreted as a 16-bit signed int, if the value is
    positive, assign the first byte to the red channel, and the second, to the
    green one, then set the blue channel to zero. If the value is negative, take
    the two's complement prior to channel assignment and set the blue channel to
    255.

    :param word: two bytes representing a 16-bit signed int
    :type word: bytes()

    :return: three integers between 0 and 255, inclusive
    :rtype: tuple()
    """
    if word[0] & 2**7:
        r = word[1] ^ 255
        g = (word[0] ^ 255) + 1
        b = 255
    else:
        r, g = word
        b = 0

    return r, g, b


def simple_decode(r, g, b):
    """Given three one-byte integers--r, g, and b, respectively--if b != 255,
    return r and g, concatenated in a bytearray. Otherwise, if b == 255, treat
    r and g as a signed, 16-bit integer, taking the little-endian two's
    complement and returning the result.

    :param r: an integer between 0 and 255
    :type r: int
    :param g: an integer between 0 and 255
    :type g: int
    :param b: an integer between 0 and 255
    :type b: int

    :return: a word (two bytes)
    :rtype: bytes()
    """
    if b == 255:
        word = bytearray([(g ^ 255) + 1])
        word += bytearray([r ^ 255])
    else:
        word = bytearray([r, g])

    return word
