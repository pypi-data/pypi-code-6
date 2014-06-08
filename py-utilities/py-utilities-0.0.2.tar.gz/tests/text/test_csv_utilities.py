#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_utilities.text.csv_utilities import csv_to_headers
from py_utilities.text.csv_utilities import csv_to_html
from py_utilities.text.csv_utilities import csv_to_list
from py_utilities.text.csv_utilities import list_to_csv
import tempfile
import unittest


class TestCsv(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.csv_headers_path = os.path.join(self.cwd, '..', 'data',
                                             'test_csv_to_list_headers.csv')
        self.csv_no_headers_path = os.path.join(
            self.cwd, '..', 'data', 'test_csv_to_list_no_headers.csv')
        self.temp_dir = tempfile.gettempdir()

    def test_csv_to_list(self):
        data = csv_to_list(self.csv_headers_path)
        ok_(len(data) == 3)
        data = csv_to_list(self.csv_no_headers_path, has_headers=False)
        ok_(len(data) == 4)

    def test_csv_to_headers(self):
        data = csv_to_headers(self.csv_headers_path)
        ok_(len(data) == 2)
        data = csv_to_headers(self.csv_no_headers_path, has_headers=False)
        ok_(len(data) == 0)

    def test_csv_to_html(self):
        html = csv_to_html(self.csv_headers_path)
        ok_(html.count("<tr>") == 4)

    def test_list_to_csv(self):
        tmp_data = [['Ryan', '1'], ['Bob', '2'], ['Foo', '3']]
        tmp_csv = os.path.join(self.temp_dir, 'csv_test')
        list_to_csv(tmp_csv, tmp_data)
        with open(tmp_csv) as f:
            for i, l in enumerate(f):
                pass
        ok_(i + 1 == len(tmp_data))

# vim: filetype=python
