#!/usr/bin/env python

# standard library imports

# third party related imports
from PIL import Image

# local library imports


def imgresize(input_filename, width=None, height=None, output_filename=None):
    """Resize an image.

    Args:
        input_filename: A string that is the filename of input image.
        width: An int that is the desired width. If it is None, the
            width is determined by the height to preserve the aspect
            ratio.
        height: An int that is the desired height. If it is None, the
            height is determined by the width to preserve the aspect
            ratio.
        output_filename: A string that is the filename of output image.
            If it is None, the input image will be resized in place.

    """

    if width is None and height is None:
        raise ValueError('width and height are None')

    img = Image.open(input_filename)
    original_width, original_height = img.size

    if width is None:
        width = int(1.0 * original_width / original_height * height + 0.5)

    if height is None:
        height = int(1.0 * original_height / original_width * width + 0.5)

    resized_img = img.resize((width, height), Image.ANTIALIAS)

    if output_filename is None:
        resized_img.save(input_filename, quality=95)
    else:
        resized_img.save(output_filename, quality=95)

