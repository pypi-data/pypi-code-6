#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import argparse


from transmedia.conversion import convert_pixels_to_bytes
from transmedia.io import read_pixels_from_png, write_data_to_file


class ConvertPixelsInPngFileToBytes():
    def __init__(self, input_file, output_file):
        """Initialize object.

        :param input_file: path to the file to convert
        :type input_file: str
        :param output_file: path to the PNG file to be written
        :type output_file: str
        """
        self._input_file = input_file
        self._output_file = output_file

    def execute(self):
        with open(self._input_file, 'rb') as png_file:
            with open(self._output_file, 'wb') as data_file:
                pixels = read_pixels_from_png(png_file)
                write_data_to_file(convert_pixels_to_bytes(pixels), data_file)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Transform PNG into bytes')
    parser.add_argument('-i', '--input', help='input PNG file', required=True)
    parser.add_argument('-o', '--output', help='output data file', required=True)
    args = parser.parse_args()

    ConvertPixelsInPngFileToBytes(args.input, args.output).execute()
