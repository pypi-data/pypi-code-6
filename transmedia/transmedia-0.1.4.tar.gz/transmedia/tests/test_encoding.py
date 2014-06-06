#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import transmedia.encoders as encoders


test_values = ((bytearray.fromhex('0000'), (int(0x00), int(0x00), int(0x00))),
               (bytearray.fromhex('1111'), (int(0x11), int(0x11), int(0x00))),
               (bytearray.fromhex('ffff'), (int(0x00), int(0x01), int(0xff))))


### simple_encode tests ###

def check_simple_encode_maps_word_to_correct_color(word, correct_color):
    test_color = encoders.simple_encode(word)

    assert test_color == correct_color, \
        "{} =! {}".format(test_color, correct_color)


def test_simple_encode_maps_words_to_correct_colors():
    for word, correct_color in test_values:
        yield(check_simple_encode_maps_word_to_correct_color, word,
              correct_color)


def test_simple_encode_raises_value_error_on_single_byte_input():
    try:
        encoders.simple_encode(bytearray.fromhex('00'))

        assert False, "simple_encoder erroneously succeeds on single-byte input"

    except ValueError:
        pass


def test_simple_encode_raises_type_error_on_int_input():
    try:
        encoders.simple_encode(1)

        assert False, "simple_encoder erroneously succeeds on integer input"

    except TypeError:
        pass


### simple_decode tests ###

def check_simple_decode_maps_color_to_correct_word(color, correct_word):
    test_word = encoders.simple_decode(*color)

    assert test_word == correct_word, "{} =! {}".format(test_word, correct_word)


def test_simple_decode_maps_colors_to_correct_words():
    for correct_word, color in test_values:
        yield(check_simple_decode_maps_color_to_correct_word, color,
              correct_word)


def test_simple_decode_raises_type_error_on_single_byte_input():
    try:
        encoders.simple_decode(0)

        assert False, "simple_decoder erroneously succeeds on single-byte input"

    except TypeError:
        pass


def test_simple_decode_raises_type_error_on_str_input():
    try:
        encoders.simple_decode('0', '0', '0')

        assert False, "simple_decoder erroneously succeeds on string input"

    except TypeError:
        pass
