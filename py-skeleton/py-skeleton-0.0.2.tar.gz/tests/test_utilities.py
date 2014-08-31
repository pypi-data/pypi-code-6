#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment
from jinja2 import FileSystemLoader
from nose.tools import eq_
from nose.tools import ok_
from nose_parameterized import parameterized
import os
from py_configurator.backends.dict import DictionaryProviderBackend
from py_configurator.config import Config
from py_skeleton.utilities import get_template_contents
from py_skeleton.utilities import iter_files_filter
from py_skeleton.utilities import resolve_templated_file_path
from py_skeleton.utilities import TEMPLATED_RE
import unittest


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.tmpl_dir = os.path.join(self.cwd, '.', 'data')

    def test_get_template_contents(self):
        loader = FileSystemLoader(self.tmpl_dir)
        env = Environment(loader=loader, keep_trailing_newline=True)
        context_dict = {"Default": {"Name": "Ryan"}}
        contents = get_template_contents(env, 'test.tmpl', context_dict)
        eq_(contents, "Hello, Ryan\n")

    def test_iter_files_filter_returns_files_with_appropriate_filter(self):
        tmp_dir = os.path.join(self.tmpl_dir, 'foo')
        num_files = 0
        for file in iter_files_filter(tmp_dir, "*.tmpl"):
            num_files += 1
        ok_(num_files == 3)

    def test_iter_files_filter_returns_no_files_with_not_found_filter(self):
        tmp_dir = os.path.join(self.tmpl_dir, 'foo')
        num_files = 0
        for file in iter_files_filter(tmp_dir, "*.conf"):
            num_files += 1
        ok_(num_files == 0)

    @parameterized.expand([
        ("/foo/bar"),
        ("/foo/bar/{foo}"),
        ("/foo/bar/{{foo"),
        ("/foo/bar/{foo}}")
    ])
    def test_tmpl_regular_expression_with_invalid_template_paths(self, path):
        m = TEMPLATED_RE.search(path)
        ok_(m is None)

    @parameterized.expand([
        ("/foo/bar/{{temp}}", "temp"),
        ("/foo/bar/{{temp.bar}}", "temp.bar"),
        ("/foo/bar/{{     temp.bar}}", "temp.bar"),
    ])
    def test_tmpl_regular_expression_with_valid_template_paths(
            self, path, config_key):
        m = TEMPLATED_RE.search(path)
        if m:
            ok_(m.group(2).strip() == config_key)

    def test_resolve_templated_file_path_with_no_match_returns_self(self):
        path = "/foo/bar/is/not/templated"
        ok_(path, resolve_templated_file_path(path, None))

    def test_resolve_templated_file_path_with_match_returns_templated(self):
        path = "/foo/bar/is/templated/{{foo}}"
        config = Config(DictionaryProviderBackend({'foo': 'bartime'}))
        ok_(path != resolve_templated_file_path(path, config))
        ok_("/foo/bar/is/templated/bartime" ==
            resolve_templated_file_path(path, config))


# vim: filetype=python
