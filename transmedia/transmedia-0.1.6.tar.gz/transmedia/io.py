#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import png

from transmedia.util import PixelArray


def read_data_from_file(file):
    """Read all data from a file into a bytearray.

    :param file: file open for binary read
    :type file: io.BufferedReader() or io.BytesIO()

    :return: bytearray of the provided file
    :rtype: bytes()
    """
    return b''.join([b for b in file])


def write_data_to_file(data, file):
    """Write data to a file.

    :param data: a bytearray
    :type data: bytes()
    :param file: target file
    :type file: io.BufferedReader() or io.BytesIO()
    """
    file.write(data)


def read_pixels_from_png(file):
    """Read pixels from a PNG file into a pixel array object.

    :param file: file open for binary read
    :type file: io.BufferedReader() or io.BytesIO()

    :return: pixel array object
    :rtype: PixelArray()
    """
    png_data = png.Reader(file).read()
    pixel_imap = png_data[2]

    return PixelArray([r.tolist() for r in pixel_imap])


def write_pixels_to_png(pixel_array, file):
    """Write rows of flat pixels to a png file.

    :param pixel_array: a pixel array object
    :type pixel_array: PixelArray()
    :param file: target png file
    :type file: io.BufferedReader() or io.BytesIO()
    """
    w = png.Writer(pixel_array.width, pixel_array.height, compression=9)
    w.write(file, pixel_array.rows)
