#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

from transmedia import encoders
from transmedia.io import (read_data_from_file, write_pixels_to_png,
                           read_pixels_from_png, write_data_to_file)

from transmedia.util import PixelArray


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


class ConversionBase():
    """Base class for all conversion objects.
    """
    def __init__(self, input_file, output_file):
        """Initialize object.

        :param input_file: path of the file to convert
        :type input_file: str
        :param output_file: path of the file to be written
        :type output_file: str
        """
        self._input_file = input_file
        self._output_file = output_file

    def execute(self):
        raise NotImplementedError("execute() method not implemented!")


class ConvertBytesInFileToPngFile(ConversionBase):
    def __init__(self, input_file, output_file, width):
        """Initialize object.

        :param input_file: path of the file to convert
        :type input_file: str
        :param output_file: path of the file to be written
        :type output_file: str
        :param width: width, in pixels, of the resulting PNG image
        :type width: int
        """
        super().__init__(input_file, output_file)
        self._width = width

    def execute(self):
        with open(self._input_file, 'rb') as data_file:
            with open(self._output_file, 'wb') as png_file:
                data = read_data_from_file(data_file)
                write_pixels_to_png(convert_bytes_to_pixels(data, self._width),
                                    png_file)


class ConvertPixelsInPngFileToBytesFile(ConversionBase):
    def __init__(self, input_file, output_file):
        """Initialize object.

        :param input_file: path of the file to convert
        :type input_file: str
        :param output_file: path of the file to be written
        :type output_file: str
        """
        super().__init__(input_file, output_file)

    def execute(self):
        with open(self._input_file, 'rb') as png_file:
            with open(self._output_file, 'wb') as data_file:
                pixels = read_pixels_from_png(png_file)
                write_data_to_file(convert_pixels_to_bytes(pixels), data_file)

