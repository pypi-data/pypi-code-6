#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from py_utilities.ui.color_utilities import random_hex_color
import re
import unittest


VALID_COLOR_RE = re.compile(r'#[a-fA-F0-9]{6}$')


class TestColorUtilities(unittest.TestCase):

    def test_random_hex_color(self):
        for x in xrange(1, 500):
            random_color = random_hex_color()
            return ok_(VALID_COLOR_RE.match(random_color))


# vim: filetype=python
