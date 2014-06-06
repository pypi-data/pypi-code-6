#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

from transmedia import encoders


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


def convert_bytes_to_pixels(data, width, encoder=encoders.simple_encode):
    """Given a target pixel width and encoding function, convert bytes to
    rows of pixels, two bytes at a time.

    :param data: bytes to encode
    :type data: iterable
    :param width: number of pixels per row
    :type width: int
    :param encoder: encoding function
    :type encoder: function()

    :return: a pixel array object
    :rtype: PixelArray()
    """
    if width < 1:
        raise ValueError("width parameter must be a positive integer")

    byte_depth = 3
    bytes_per_pixel = 2
    data_idx = 0
    rows = []
    try:
        while True:
            cur_row = []
            while len(cur_row) < (width * byte_depth):
                word = data[data_idx:data_idx + bytes_per_pixel]
                if len(word) < bytes_per_pixel:
                    if len(cur_row) > 0:
                        rows += [cur_row]

                    raise ValueError()

                cur_row += encoder(word)
                data_idx += bytes_per_pixel

            rows += [cur_row]

    except ValueError:
        pass

    return PixelArray(rows, byte_depth=byte_depth)


def convert_pixels_to_bytes(pixel_array, encoder=encoders.simple_decode):
    """Given a pixel array and an encoding function, convert all pixels
    to a byte array.

    :param pixel_array: a pixel array object
    :type pixel_array: PixelArray()
    :param encoder: encoding function
    :type encoder: function()

    :return: a bytearray
    :rtype: bytes()
    """
    words = bytearray()
    for row in pixel_array:
        byte_idx = 0
        while byte_idx < len(row) - 1:
            try:
                components = row[byte_idx:byte_idx + pixel_array.byte_depth]
                words += encoder(*components)
                byte_idx += pixel_array.byte_depth

            except ValueError:
                break

    return words
