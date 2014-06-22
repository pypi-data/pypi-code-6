#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nose.tools import eq_
import os
from py_utilities.context_managers import cd
import tempfile
import unittest


class TestContextManagers(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.gettempdir()

    def test_cd(self):
        curr = os.getcwd()
        path = os.path.realpath(self.temp_dir)
        with cd(path):
            cwd = os.getcwd()
            ok_(curr != cwd)
            eq_(cwd, path)
        cwd = os.getcwd()
        eq_(curr, cwd)

# vim: filetype=python
