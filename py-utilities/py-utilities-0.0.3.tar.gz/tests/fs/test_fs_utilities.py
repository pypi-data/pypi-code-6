#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..helpers import write_file_contents
from nose.tools import ok_
from nose.tools import raises
import os
from py_utilities.fs.fs_utilities import mkdir_p
from py_utilities.fs.fs_utilities import rm_if_exists
from py_utilities.fs.fs_utilities import rm_rf
from py_utilities.fs.fs_utilities import safe_stat
from py_utilities.fs.fs_utilities import touch
import shutil
import tempfile
import unittest


class TestFs(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = tempfile.gettempdir()

    def tearDown(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        if os.path.exists(tmp_foo):
            shutil.rmtree(tmp_foo)

    def test_mkdir_p(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        tmp_foo_bar = os.path.join(self.temp_dir, 'foo', 'bar')
        tmp_foo_bar_rules = os.path.join(self.temp_dir, 'foo', 'bar', 'rules')
        mkdir_p(tmp_foo_bar_rules)
        ok_(os.path.exists(tmp_foo))
        ok_(os.path.exists(tmp_foo_bar))
        ok_(os.path.exists(tmp_foo_bar_rules))

    @raises(OSError)
    def test_mkdir_p_raise_exception(self):
        tmp_foo_bar_rules = os.path.join(self.temp_dir, 'foo', 'bar', 'rules')
        mkdir_p(tmp_foo_bar_rules)
        tmp_file = os.path.join(tmp_foo_bar_rules, 'file')
        f = open(tmp_file, 'w')
        f.close()
        mkdir_p(tmp_file)

    def test_mkdir_p_should_not_raise_exception(self):
        tmp_foo_bar_rules = os.path.join(self.temp_dir, 'foo', 'bar', 'rules')
        mkdir_p(tmp_foo_bar_rules)
        mkdir_p(tmp_foo_bar_rules)

    def test_rm_rf(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        tmp_foo_bar = os.path.join(self.temp_dir, 'foo', 'bar')
        tmp_foo_bar_rules = os.path.join(self.temp_dir, 'foo', 'bar', 'rules')
        os.mkdir(tmp_foo)
        os.mkdir(tmp_foo_bar)
        os.mkdir(tmp_foo_bar_rules)
        rm_rf(tmp_foo)
        ok_(not os.path.exists(tmp_foo))
        ok_(not os.path.exists(tmp_foo_bar))
        ok_(not os.path.exists(tmp_foo_bar_rules))

    def test_rm_if_exists(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        os.mkdir(tmp_foo)
        tmp_foo_bar = os.path.join(self.temp_dir, 'foo', 'bar')
        write_file_contents(tmp_foo_bar, "BAR")
        rm_if_exists(tmp_foo_bar)
        ok_(not os.path.exists(tmp_foo_bar))

    @raises(OSError)
    def test_rm_if_exists_should_raise_exception_with_dir(self):
        tmp_foo = os.path.join(self.temp_dir, 'foo')
        os.mkdir(tmp_foo)
        rm_if_exists(tmp_foo)

    def test_safe_stat(self):
        tmp_foo = os.path.join(self.temp_dir, 'fooness')
        write_file_contents(tmp_foo, 'blah')
        ok_(safe_stat(tmp_foo).st_size > 0)

    def test_safe_stat_on_non_existent_file_should_not_raise_os_error(self):
        tmp_foo = os.path.join(self.temp_dir, 'foodoesnotexist')
        ok_(safe_stat(tmp_foo) is None)

    def test_touch(self):
        file = os.path.join(self.cwd, 'test_fs_utilities.py')
        curr_access_time = os.path.getmtime(file)
        touch(file)
        new_access_time = os.path.getmtime(file)
        ok_(new_access_time > curr_access_time)

# vim: filetype=python
