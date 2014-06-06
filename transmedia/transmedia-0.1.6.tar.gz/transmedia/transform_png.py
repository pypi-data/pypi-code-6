#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import argparse

from transmedia.conversion import (ConvertBytesInFileToPngFile,
                                   ConvertPixelsInPngFileToBytesFile)

from transmedia.util import calculate_output_png_width_from_file


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
