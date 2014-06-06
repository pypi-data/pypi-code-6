#-*- coding: utf-8 -*-
#
# Copyright © 2014 Jonathan Storm <the.jonathan.storm@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING.WTFPL file for more details.

__author__ = 'jstorm'

import io

from transmedia.conversion import PixelArray
from transmedia.io import (write_data_to_file, write_pixels_to_png)


def test_write_png_produces_file_of_expected_size():
    expected_size = 77  # Precomputed size of resulting PNG
    white = [255, 255, 255]
    black = [0, 0, 0]
    pixel_rows = [black + white + black,
                  white + black + white,
                  black + white + black]

    pixel_array = PixelArray(pixel_rows)
    file = io.BytesIO()
    write_pixels_to_png(pixel_array, file)

    assert len(file.getvalue()) == expected_size


def test_write_data_produces_expected_output():
    data = bytearray.fromhex('ffffe3990012')
    file = io.BytesIO()
    write_data_to_file(data, file)

    assert file.getvalue() == data
