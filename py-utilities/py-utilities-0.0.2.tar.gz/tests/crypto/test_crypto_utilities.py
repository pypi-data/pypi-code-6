#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from py_utilities.crypto.crypto_utilities import hash_password
from py_utilities.crypto.crypto_utilities import verify_password
import unittest


class TestCryptoUtilities(unittest.TestCase):

    def test_scrypt(self):
        hash = hash_password('foobar', .005)
        ok_(verify_password(hash, 'foobar', .05) is True)
        ok_(verify_password(hash, 'foobar2', .05) is False)

# vim: filetype=python
