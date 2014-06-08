#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..helpers import write_file_contents
from nose.tools import eq_
from nose.tools import ok_
import os
from py_utilities.fs.file_utilities import concat
from py_utilities.fs.file_utilities import copy_file
from py_utilities.fs.file_utilities import crc32
from py_utilities.fs.file_utilities import write_file
import shutil
import StringIO
import tempfile
import unittest


class TestFileUtilities(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = tempfile.gettempdir()
        self.test_file = os.path.join(self.cwd, '..', 'data',
                                      'test_csv_to_list_headers.csv')

    def tearDown(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        if os.path.exists(tmp_foo):
            shutil.rmtree(tmp_foo)

    def test_concat(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        tmp_foo_bar = os.path.join(self.temp_dir, 'foo', 'bar')
        tmp_foo_rules = os.path.join(self.temp_dir, 'foo', 'rules')
        os.mkdir(tmp_foo)
        write_file_contents(tmp_foo_bar, "BAR\n")
        write_file_contents(tmp_foo_rules, "RULES\n")
        output = StringIO.StringIO()
        concat([tmp_foo_bar, tmp_foo_rules], output)
        eq_(output.getvalue(), "BAR\nRULES\n")

    def test_copy_file(self):
        output = StringIO.StringIO()
        copy_file(self.test_file, output)
        eq_(output.getvalue(), 'Name,Age\nRyan,21\nBob,22\nJoe,23\n')

    def test_crc32(self):
        crc = crc32(os.path.join(self.cwd, './data/foobar.txt'))
        ok_(crc == 'ECEFF2A5')

    def test_write_file(self):
        tmp_file = os.path.join(self.temp_dir, 'file')
        write_file(tmp_file, "Hello World")
        with open(tmp_file, 'r') as f:
            content = f.read()
        eq_(content, "Hello World")

# vim: filetype=python
