#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nose.tools import raises
from py_utilities.text.string_utilities import str_to_bool
import unittest


class TestStringUtilities(unittest.TestCase):

    def test_str_to_bool(self):
        ok_(str_to_bool("yes"))
        ok_(str_to_bool("y"))
        ok_(str_to_bool("true"))
        ok_(str_to_bool("t"))
        ok_(str_to_bool("1"))
        ok_(not str_to_bool("no"))
        ok_(not str_to_bool("n"))
        ok_(not str_to_bool("false"))
        ok_(not str_to_bool("f"))
        ok_(not str_to_bool("0"))
        ok_(not str_to_bool("0.0"))
        ok_(not str_to_bool(""))
        ok_(not str_to_bool("none"))
        ok_(not str_to_bool("[]"))
        ok_(not str_to_bool("{}"))

    @raises(ValueError)
    def test_str_to_bool_should_raise_value_error(self):
        str_to_bool("asdfdfa")


# vim: filetype=python
