#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import argparse

from transmedia.conversion import (convert_bytes_to_pixels,
                                   convert_pixels_to_bytes)

from transmedia.io import (read_data_from_file, write_pixels_to_png,
                           read_pixels_from_png, write_data_to_file)

from transmedia.util import calculate_output_png_width_from_file


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


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Transform bytes into PNG or vice versa')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)
    args = parser.parse_args()

    if args.input.endswith(".png"):
        ConvertPixelsInPngFileToBytesFile(args.input, args.output).execute()

    elif args.output.endswith(".png"):
        png_width = calculate_output_png_width_from_file(args.input)
        ConvertBytesInFileToPngFile(args.input, args.output, png_width).execute()
    else:
        raise ValueError("Either the input or output file must end in '.png'")
