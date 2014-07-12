#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import raises
import os
from py_configurator.backends.base import ConfigException
from py_configurator.backends.ini import IniProviderBackend
import unittest


class TestIniProviderBackend(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.ini_file = os.path.join(self.cwd, '.', 'data', 'foobar.ini')
        self.invalid_ini_file = os.path.join(self.cwd, '.', 'data',
                                             'foobar-invalid.ini')

    def test_ini(self):
        provider = IniProviderBackend(self.ini_file)
        eq_('1', provider.get('Foo.Bar', None))
        eq_("Config Data", provider.get('Bar.Foo', None))
        eq_(None, provider.get('Bar', None))
        provider.delete('Foo.Bar')
        eq_(None, provider.get('Foo.Bar', None))
        provider.set('Foo.Bar', '2')
        eq_('2', provider.get('Foo.Bar', None))

        # New
        provider.set('FoosBallSection.Price', '$.50')
        eq_('$.50', provider.get('FoosBallSection.Price', None))

    @raises(ConfigException)
    def test_ini_with_invalid_delete_should_raise_exception(self):
        provider = IniProviderBackend(self.ini_file)
        provider.delete('Foo')

    @raises(ConfigException)
    def test_invalid_ini_should_raise_exception(self):
        IniProviderBackend(self.invalid_ini_file)

    @raises(ConfigException)
    def test_non_existent_ini_should_raise_exception(self):
        IniProviderBackend("skfdjaskldjalksdfjasklfaf")

# vim: filetype=python
