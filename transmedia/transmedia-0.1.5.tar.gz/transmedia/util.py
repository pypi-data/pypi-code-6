#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import math
import os


def integer_side_len_of_smallest_square_containing_n_units(n):
    return int(math.ceil(math.sqrt(n)))


def calculate_output_png_width_from_file(filename):
    bytes_per_word = 2
    word_count = os.path.getsize(filename) / bytes_per_word

    return integer_side_len_of_smallest_square_containing_n_units(word_count)
