#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_configurator.backends import get_provider
from py_configurator.backends.ini import IniProviderBackend
import unittest


class TestProviderBackend(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.ini_file = os.path.join(self.cwd, '.', 'data', 'foobar.ini')

    def test_get_provider(self):
        provider = get_provider(self.ini_file)
        ok_(type(provider) == IniProviderBackend)


# vim: filetype=python
