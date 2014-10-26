#!/usr/bin/env python
# coding=utf-8

"""
test_pcf_decrypt
----------------------------------

Tests for `pcf_decrypt` module.
"""

from . import os, hashlib, unittest

import binascii

import pcf_decrypt as m


class TestPcfDecrypt(unittest.TestCase):
    def test_sha1_bytes(self):
        r = os.urandom(64)
        hashlib_hash = hashlib.sha1(r).digest()
        package_hash = m._sha1(r)

        self.assertEqual(hashlib_hash, package_hash)

    def test_sha1_hexstr(self):
        r = binascii.b2a_hex(os.urandom(64))
        hashlib_hash = hashlib.sha1(r).digest()
        package_hash = m._sha1(r)

        self.assertEqual(hashlib_hash, package_hash)

    def test_decrypt(self):
        enc = "D06615FC4D2046942A6F39951FC40794740E30C485090B4416C9D5A65DE59E" \
              "5230A63D391F2A634820B574A37E16DB23820C89CD29DA2245"
        plaintext = 'Sh@r3dK3ySP*&%$'

        self.assertEqual(m.decrypt(enc), plaintext)

    def test_notvalid_type(self):
        with self.assertRaises(m.PcfDecryptionError):
            m.decrypt([])

    def test_notvalid_length(self):
        with self.assertRaises(m.PcfDecryptionError):
            m.decrypt(b'')

    def test_notvalid_checksum(self):
        with self.assertRaises(m.PcfDecryptionError):
            m.decrypt(os.urandom(48))

if __name__ == '__main__':
    unittest.main()
