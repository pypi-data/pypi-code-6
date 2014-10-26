#!/usr/bin/env python
# coding=utf-8

"""
test_command_line
----------------------------------

Tests for `pcf_decrypt.__main__` module.
"""

import sys
import binascii
from contextlib import contextmanager

# from . import os, codecs, hashlib, unittest, m
from . import os, unittest

from six import PY3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO

import pcf_decrypt.__main__ as m


class TestCommandLine(unittest.TestCase):
    @contextmanager
    def assertPrints(self, out=''):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr

        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield
        finally:
            sys.stdout, sys.stderr = old_out, old_err

        output = '\n'.join([
            new_out.getvalue().strip(),
            new_err.getvalue().strip(),
        ]).strip()

        self.assertEqual(output, out.strip())

    def test_files_or_hash_file(self):
        f = os.path.realpath(__file__)

        self.assertEqual(m._file_or_hash(f), ('file', f))

    def test_files_or_hash_hash(self):
        enc = "D06615FC4D2046942A6F39951FC40794740E30C485090B4416C9D5A65DE59" \
              "E5230A63D391F2A634820B574A37E16DB23820C89CD29DA2245"
        data = binascii.a2b_hex(enc)

        self.assertEqual(m._file_or_hash(enc), ('hash', data))

    def test_files_or_hash_neither(self):
        import argparse
        with self.assertRaises(argparse.ArgumentTypeError):
            m._file_or_hash('test')

        with self.assertRaises(argparse.ArgumentTypeError):
            m._file_or_hash('ab')

    def test_help(self):
        with self.assertPrints("""
usage: pcf_decrypt [-h] file_or_hash [file_or_hash ...]

Decrypt encryped passwords in Cisco pcf files

positional arguments:
  file_or_hash  File to parse or hash to decode

optional arguments:
  -h, --help    show this help message and exit

Arguments can either be a pcf file with at least one enc_FIELD field within to
decrypt or an encrypted hash to decrypt. If any hashes are present (determined
if the operating system say it's not a path to a file and can be successfully
decoded from a hex string to a byte array), they will be outputted in order
presented first, followed by any files in the form: filename:FIELD:plaintext
        """):
            with self.assertRaises(SystemExit):
                m.get_args('-h')

    def test_too_few_arguments(self):
        if PY3:
            with self.assertPrints("""
usage: pcf_decrypt [-h] file_or_hash [file_or_hash ...]
pcf_decrypt: error: the following arguments are required: file_or_hash
            """):
                with self.assertRaises(SystemExit):
                    m.get_args([])
        else:
            with self.assertPrints("""
usage: pcf_decrypt [-h] file_or_hash [file_or_hash ...]
pcf_decrypt: error: too few arguments
            """):
                with self.assertRaises(SystemExit):
                    m.get_args([])

    def test_not_valid_param(self):
        with self.assertPrints("""
usage: pcf_decrypt [-h] file_or_hash [file_or_hash ...]
pcf_decrypt: error: argument file_or_hash: 'test' is not a file or a hash
        """):
            with self.assertRaises(SystemExit):
                m.get_args('test')

        with self.assertPrints("""
usage: pcf_decrypt [-h] file_or_hash [file_or_hash ...]
pcf_decrypt: error: argument file_or_hash: 'ab' is not a long enough hash to be an encrypted password
        """):
            with self.assertRaises(SystemExit):
                m.get_args('ab')

    def test_main(self):
        enc = "D06615FC4D2046942A6F39951FC40794740E30C485090B4416C9D5A65DE59E" \
              "5230A63D391F2A634820B574A37E16DB23820C89CD29DA2245"
        with self.assertPrints('Sh@r3dK3ySP*&%$'):
            m.main(enc)

        with self.assertPrints(""):
            m.main(__file__)

if __name__ == '__main__':
    unittest.main()
