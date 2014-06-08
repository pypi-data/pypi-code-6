#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_utilities.fs.path_utilities import expanded_abspath
from py_utilities.fs.path_utilities import filename
from py_utilities.fs.path_utilities import get_first_dir_path
from py_utilities.fs.path_utilities import get_first_file_path
import tempfile
import unittest


class TestPath(unittest.TestCase):

    def test_expanded_abspath(self):
        home = os.environ["HOME"]
        ok_(expanded_abspath("~") == home)
        ok_(expanded_abspath("~/foo") == os.path.join(home, 'foo'))
        ok_(expanded_abspath("/foo") == "/foo")
        ok_(expanded_abspath("/foo/bar") == "/foo/bar")

    def test_filename(self):
        paths = ['/foo/bar/', '/foo/bar', 'foo/bar/', 'foo/bar',
                 '\\foo\\bar\\', '\\foo\\bar', 'foo\\bar\\', 'foo\\bar']
        for path in paths:
            ok_(filename(path) == 'bar')

    def test_get_first_dir_path(self):
        dir = tempfile.mkdtemp()
        home = os.environ["HOME"]
        fake = '/foo/bar/x/y/z/a'
        ok_(dir == get_first_dir_path([dir]))
        ok_(dir == get_first_dir_path([dir, home]))
        ok_(home == get_first_dir_path([home, dir]))
        ok_(home == get_first_dir_path([fake, home, dir]))
        ok_(dir == get_first_dir_path([fake, dir, home]))

    def test_get_first_file_path(self):
        f = tempfile.mkstemp()[1]
        fake = '/foo/bar/x/y/z/a'
        ok_(f == get_first_file_path([f]))
        ok_(f == get_first_file_path([f, fake]))
        ok_(f == get_first_file_path([fake, f]))


# vim: filetype=python
