#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_utilities.text.text_utilities import lines
from py_utilities.text.text_utilities import strip_if_true
import unittest


class TestText(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.csv_headers_path = os.path.join(self.cwd, '..', 'data',
                                             'test_csv_to_list_headers.csv')

    def test_lines(self):
        list_of_lines = lines(self.csv_headers_path, strip=False)
        ok_(len(list_of_lines) == 4)
        ok_(list_of_lines[0] == "Name,Age\n")
        list_of_lines = lines(self.csv_headers_path, strip=True)
        ok_(len(list_of_lines) == 4)
        ok_(list_of_lines[0] == "Name,Age")
        list_of_lines = lines(self.csv_headers_path)
        ok_(list_of_lines[0] == "Name,Age")

    def test_strip_if_true(self):
        test_with_spaces = " T es t "
        test_without_spaces = "T es t"
        test_stripped = strip_if_true(test_with_spaces, True)
        test_not_stripped = strip_if_true(test_with_spaces, False)
        ok_(test_without_spaces == test_stripped)
        ok_(test_with_spaces == test_not_stripped)


# vim: filetype=python
