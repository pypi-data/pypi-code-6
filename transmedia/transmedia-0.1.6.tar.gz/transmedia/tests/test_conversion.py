#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

from transmedia.conversion import (convert_bytes_to_pixels,
                                   convert_pixels_to_bytes)

import transmedia.encoders as encoders


### bytes2pixels tests ###

def check_bytes2pixels_returns_correct_width(correct_width):
    data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
    pixels = convert_bytes_to_pixels(data, correct_width,
                                     encoders.simple_encode)

    width_top = len(pixels.rows[0]) / pixels.byte_depth
    width_bottom = len(pixels.rows[-1]) / pixels.byte_depth

    assert width_top == width_bottom == correct_width, \
        "({} == {} == {}) is false".format(width_top, width_bottom,
                                           correct_width)


def test_bytes2pixels_returns_correct_width():
    for width in (1, 3, 9):  # a single column, a square, a single row
        yield check_bytes2pixels_returns_correct_width, width


def test_bytes2pixels_returns_square():
    correct_dimension = 3  # 3x3 square
    data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
    pixels = convert_bytes_to_pixels(data, correct_dimension,
                                     encoders.simple_encode)

    width_top = len(pixels.rows[0]) / pixels.byte_depth
    height = len(pixels.rows)

    assert width_top == height == correct_dimension, \
        "({} == {} == {} == {}) is false".format(width_top, height,
                                                 correct_dimension)


def test_bytes2pixels_raises_value_error_on_negative_width():
    try:
        negative_width = -1
        data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
        convert_bytes_to_pixels(data, negative_width, encoders.simple_encode)

        assert False, "bytes2pixels erroneously succeeds on negative width"

    except ValueError:
        pass


def test_bytes2pixels_raises_value_error_on_zero_width():
    try:
        zero_width = 0
        data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
        convert_bytes_to_pixels(data, zero_width, encoders.simple_encode)

        assert False, "bytes2pixels erroneously succeeds on zero width"

    except ValueError:
        pass


def test_bytes2pixels_returns_max_width_on_excessive_width_input():
    data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
    max_width = len(data) // 2
    excessive_width = max_width + 1
    pixels = convert_bytes_to_pixels(data, excessive_width,
                                     encoders.simple_encode)

    assert pixels.width != excessive_width, \
        "{} == {} == {}".format(pixels.width, excessive_width)


### pixels2bytes tests ###

def test_pixels2bytes_returns_correct_length():
    data = bytearray.fromhex('ffff6d06cb0cc436103c2741895c1f5f4861')
    correct_length = len(data)
    width = 3
    test_png_data = convert_bytes_to_pixels(data, width, encoders.simple_encode)
    words = convert_pixels_to_bytes(test_png_data, encoders.simple_decode)

    assert len(words) == correct_length, \
        "{} != {}".format(len(words), correct_length)
