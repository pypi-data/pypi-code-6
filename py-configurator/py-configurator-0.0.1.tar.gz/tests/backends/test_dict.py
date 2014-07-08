#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from py_configurator.backends.dict import DictionaryProviderBackend
import unittest


class TestDictionaryProviderBackend(unittest.TestCase):

    def test_dict(self):
        dict = {'foo': 'bar', 'too': 'much'}
        provider = DictionaryProviderBackend(dict)
        provider.set('python', 'rules')
        eq_('bar', provider.get('foo', None))
        eq_(None, provider.get('foo2', None))
        eq_(1, provider.get('foo3', 1))
        eq_('rules', provider.get('python', None))
        provider.delete('python')
        eq_(-1, provider.get('python', -1))


# vim: filetype=python
