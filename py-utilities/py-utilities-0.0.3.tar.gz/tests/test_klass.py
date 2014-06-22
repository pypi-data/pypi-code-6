#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
import os
from py_utilities.klass import get_func_from_file
from py_utilities.klass import get_klass_from_file
import unittest


class Test(object):
    pass


def test_func():
    return 1 + 2


class TestKlass(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.test_files = ['test_klass.py', 'test_klass.pyc']

    def test_get_func_from_file(self):
        for t in self.test_files:
            func = get_func_from_file(os.path.join(self.cwd, t), 'test_func')
            eq_(func(), 3)

    def test_get_klass_from_file(self):
        for t in self.test_files:
            klass = get_klass_from_file(os.path.join(self.cwd, t), 'Test')
            eq_(type(Test), type(klass))

# vim: filetype=python
