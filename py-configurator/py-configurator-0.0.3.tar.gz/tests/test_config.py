#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
from nose.tools import eq_
from py_configurator.config import Config
import unittest


class TestConfig(unittest.TestCase):

    @patch('py_configurator.backends.base.BaseProviderBackend')
    def test_config_get_with_mock_provider(self, mock_provider):
        mock_provider.get.return_value = "Foo"
        config = Config(mock_provider)
        eq_(config.get("bar"), "Foo")
        mock_provider.get.assert_called_once_with("bar", None)

    @patch('py_configurator.backends.base.BaseProviderBackend')
    def test_config_set_with_mock_provider(self, mock_provider):
        config = Config(mock_provider)
        config.set("boo", "moo")
        mock_provider.set.assert_called_once_with("boo", "moo")


# vim: filetype=python
