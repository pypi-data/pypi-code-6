#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import ok_
import os
from py_configurator import Locator
import unittest


class TestLocator(unittest.TestCase):

    def test_locator_construction(self):
        config_name = 'foo.bar'
        local_dir = './'
        system_dir = '/foo/bar/tmp'
        env_key = 'CONFIG_KEY'

        locator = Locator(
            env_key=env_key,
            config_name=config_name,
            local_dir=local_dir,
            system_dir=system_dir)

        eq_(locator.config_name, config_name)
        eq_(locator.local_dir, local_dir)
        eq_(locator.env_key, env_key)

        config_name_2 = 'foo.bar.2'
        local_dir_2 = '/foo/bar/tmp/2'
        env_key_2 = 'CONFIG_KEY_2'
        locator.config_name = config_name_2
        locator.local_dir = local_dir_2
        locator.env_key = env_key_2

        eq_(locator.config_name, config_name_2)
        eq_(locator.local_dir, local_dir_2)
        eq_(locator.env_key, env_key_2)

    def test_config_locator_get_config_search_paths(self):
        config_name = 'foo.bar'
        local_dir = './'
        system_dir = '/foo/bar/tmp'
        env_key = 'CONFIG_KEY'
        env_key_path = '/bar/config.path'

        os.environ[env_key] = env_key_path

        locator = Locator(
            env_key=env_key,
            config_name=config_name,
            local_dir=local_dir,
            system_dir=system_dir)

        config_search_paths = locator.get_config_paths()

        ok_(env_key_path in config_search_paths)
        ok_(os.path.join('./', config_name) in config_search_paths)
        ok_('/foo/bar/tmp/foo.bar' in config_search_paths)
        ok_(os.path.join(os.path.expanduser("~"), config_name) in
            config_search_paths)


# vim: filetype=python
