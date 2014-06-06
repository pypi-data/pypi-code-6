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


class PixelArray():
    """Value object with some convenient behavior and properties for rows of
    flat pixels.
    """
    def __init__(self, pixel_rows, byte_depth=3):
        """Initialize new PixelArray object.

        :param pixel_rows: an array of rows of flat pixels
        :type pixel_rows: iterable containing one or more list[int]
        """
        self._byte_depth = byte_depth
        self._pixel_rows = pixel_rows
        self._height = len(pixel_rows)
        self._width = len(max(pixel_rows, key=len)) // self._byte_depth

    def __iter__(self):
        for r in self._pixel_rows:
            # Fill in any missing pixels with black (0, 0, 0)
            pad = [0 for i in range((self._width * self._byte_depth) - len(r))]
            yield r + pad

    @property
    def byte_depth(self):
        return self._byte_depth

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def rows(self):
        # Return rows padded with zeros
        return [r for r in self]

    @property
    def rows_raw(self):
        # Return unpadded rows
        return self._pixel_rows
