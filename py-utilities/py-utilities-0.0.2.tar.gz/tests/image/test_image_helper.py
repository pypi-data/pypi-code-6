#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from nose.tools import ok_
from py_utilities.image.image_helper import Size
import random
import unittest


class TestImageHelper(unittest.TestCase):

    def test_size_obj(self):
        rand_width = random.random()
        rand_height = random.random()
        rand_width_height_tuple = (rand_width, rand_height)
        size_obj = Size(rand_width_height_tuple)
        ok_(size_obj.width == rand_width)
        ok_(size_obj.height == rand_height)
        ok_(size_obj.size == rand_width_height_tuple)

    def test_size_obj_with_known_inputs(self):
        tuples = [((4, 3), Decimal('1.33')),
                  ((2, 1), Decimal('2.00')),
                  ((3, 2), Decimal('1.50'))]
        for tuple_pair in tuples:
            tuple = tuple_pair[0]
            aspect_ratio_as_decimal = tuple_pair[1]
            size_obj = Size(tuple)
            ok_(size_obj.width == tuple[0])
            ok_(size_obj.height == tuple[1])
            ok_(size_obj.size == (tuple[0], tuple[1]))
            ok_(size_obj.aspect_ratio_as_tuple == (tuple[0], tuple[1]))
            ok_(size_obj.aspect_ratio_as_decimal == aspect_ratio_as_decimal)

# vim: filetype=python
