#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..math.math_utilities import gcd
from decimal import Decimal


class Size(object):
    def __init__(self, size_tuple):
        self._width = float(size_tuple[0])
        self._height = float(size_tuple[1])

    @property
    def aspect_ratio_as_decimal(self):
        return Decimal('%.2f' % (float(self.width) / self.height))

    @property
    def aspect_ratio_as_tuple(self):
        d = gcd(self.width, self.height)
        return (int(self.width//d), int(self.height//d))

    @property
    def height(self):
        return self._height

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def width(self):
        return self._width


# vim: filetype=python
