#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import raises
import os
from py_configurator.backends.base import ConfigException
from py_configurator.backends.yaml import YamlProviderBackend
import tempfile
import unittest


class TestYamlProviderBackend(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.yml_file = os.path.join(self.cwd, '.', 'data', 'foobar.yml')
        self.temp_file = tempfile.TemporaryFile()

    def test_yml(self):
        provider = YamlProviderBackend(self.yml_file)
        eq_(1, provider.get('Foo.Bar', None))
        eq_("Config Data", provider.get('Bar.Foo', None))
        eq_(None, provider.get('Bar2', None))
        provider.delete('Foo.Bar')
        eq_(None, provider.get('Foo.Bar', None))
        provider.set('Foo.Bar', '2')
        eq_('2', provider.get('Foo.Bar', None))

        # New
        provider.set('Foo', 'Ball')
        eq_('Ball', provider.get('Foo', None))

    @raises(ConfigException)
    def test_yml_invalid_set_should_raise_exception(self):
        provider = YamlProviderBackend(self.yml_file)
        provider.set(None, None)

    @raises(ConfigException)
    def test_yml_invalid_delete_should_raise_exception(self):
        provider = YamlProviderBackend(self.yml_file)
        provider.delete(None)

    @raises(ConfigException)
    def test_invalid_yml_location_should_raise_exception(self):
        YamlProviderBackend('/foo/bar')


# vim: filetype=python
