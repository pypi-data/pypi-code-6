#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from py_utilities.http.url_utilities import join
import unittest


class TestUrl(unittest.TestCase):

    def test_join(self):
        eq_(join(), '')
        eq_(join('/foo'), '/foo')
        eq_(join('', ''), '')
        eq_(join('', '', '', ''), '')
        eq_(join('http://foo.com/', '/foo'), 'http://foo.com/foo')
        eq_(join('http://foo.com/', '/foo/'), 'http://foo.com/foo/')
        eq_(join('http://foo.com/', '/foo/', 'bar'), 'http://foo.com/foo/bar')
        eq_(join('http://foo.com/', 'foo', 'bar/'), 'http://foo.com/foo/bar/')
        eq_(join('http://foo.com/', 'foo', 'bar'), 'http://foo.com/foo/bar')
        eq_(join('http://foo.com/', 'foo', ''), 'http://foo.com/foo')
        eq_(join('http://foo.com/', '  ', 'foo', ''), 'http://foo.com/foo')
        eq_(join('http://foo.com/', '  ', 'foo/', ''), 'http://foo.com/foo/')

# vim: filetype=python
