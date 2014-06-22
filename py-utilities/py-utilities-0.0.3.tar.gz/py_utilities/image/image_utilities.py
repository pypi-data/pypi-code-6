#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .image_helper import Size


def aspect_ratio(size):
    """
    Returns the aspect ratio of a size tuple

    >>> aspect_ratio((800, 600))
    (4, 3)

    >>> aspect_ratio((800, 400))
    (2, 1)

    >>> aspect_ratio((2, 1))
    (2, 1)
    """
    return Size(size).aspect_ratio_as_tuple


# vim: filetype=python
