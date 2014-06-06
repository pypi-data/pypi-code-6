#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import argparse
import os

from transmedia.conversion import convert_bytes_to_pixels
from transmedia.io import read_data_from_file, write_pixels_to_png

from transmedia import util


class ConvertFileInBytesToPngFile():
    def __init__(self, input_file, output_file, width):
        """Initialize object.

        :param input_file: path to the file to convert
        :type input_file: str
        :param output_file: path to the PNG file to be written
        :type output_file: str
        :param width: width, in pixels, of the resulting PNG image
        :type width: int
        """
        self._input_file = input_file
        self._output_file = output_file
        self._width = width

    def execute(self):
        with open(self._input_file, 'rb') as data_file:
            with open(self._output_file, 'wb') as png_file:
                data = read_data_from_file(data_file)
                write_pixels_to_png(convert_bytes_to_pixels(data, self._width),
                                    png_file)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Transform bytes into PNG')
    parser.add_argument('-i', '--input', help='input data file', required=True)
    parser.add_argument('-o', '--output', help='output PNG file', required=True)
    args = parser.parse_args()

    # Calculate output png width. Number of pixels equals the number of words
    word_count = os.path.getsize(args.input) / 2
    png_width = util.side_len_of_smallest_square_containing_n_units(word_count)

    ConvertFileInBytesToPngFile(args.input, args.output, png_width).execute()
