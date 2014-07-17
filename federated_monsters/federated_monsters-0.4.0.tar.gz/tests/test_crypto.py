#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_crypto
-----------

Tests for ``crypto`` module.
"""

import unittest

import Crypto
from federated_monsters import crypto


class CryptoTest(unittest.TestCase):

    """A unit test for the ``crypto`` module."""

    def test_encrypt(self):
        pwd = "gentoo"
        txt = ">install gentoo"
        key = crypto.gen_key(pwd)

        cipher = crypto.encrypt(txt, key[0])

        plain = crypto.decrypt(cipher, key[0])

        self.assertEqual(txt, plain)
