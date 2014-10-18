# coding: utf-8

from unittest import TestCase


class TestDecimalize(TestCase):
    def _getClass(self, *args, **kwargs):
        from .decimalize import Decimalize
        return Decimalize(*args, **kwargs)

    def test_hex(self):
        dm = self._getClass('0123456789abcdef')
        self.assertEqual(dm.encode(255), 'ff')
        self.assertEqual(dm.decode('ffff'), 65535)

    def test_multibyte(self):
        dm = self._getClass(u'あいうえおかきくけこ')
        self.assertEqual(dm.encode(25), u'うか')
        self.assertEqual(dm.decode(u'くえ'), 73)

    def test_charset_error(self):
        from .exceptions import CharsetNotUniqueError
        with self.assertRaises(CharsetNotUniqueError):
            self._getClass('abca')  # not unique

    def test_decode_error(self):
        from .exceptions import DecodeError

        dm = self._getClass('abcdef')
        with self.assertRaises(DecodeError):
            dm.decode('aceg')
