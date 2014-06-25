#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PyMBFL testing suite"""


__author__ = "Dmitry Selyutin"
__license__ = "GNU LGPL"
__maintainer__ = "Dmitry Selyutin"
__email__ = "ghostmansd@solidlab.ru"


import logging
import os
import random
import sys
import unittest

import const
import core


_self_dir = os.path.dirname(__file__)
_tests_dir = os.path.join(_self_dir, "tests")


class TestPyMBFL(unittest.TestCase):
    """Run PyMBFL testing suite."""

    def test_encodings(self):
        """Try to iterate through names of multi-byte encodings."""
        for encoding in const.ENCODINGS:
            encoding = core.Encoding(encoding)

    def test_detector(self):
        """Check all available multi-byte detectors."""
        maxlen = max([len(str(i)) for i in const.ENCODINGS])
        wrong_guesses = []
        for encoding in [core.Encoding(i) for i in const.ENCODINGS]:
            exists = False
            detector = core.Detector(language=None, encodings=[encoding])
            aliases = ([encoding] + encoding.aliases)
            aliases += [i.replace('_', '-') for i in encoding.aliases]
            aliases += [i.replace('-', '') for i in encoding.aliases]
            aliases = set(aliases)
            for alias in aliases:
                path = os.path.join(_tests_dir, str(encoding))
                if os.path.exists(path):
                    exists = True
                    break
            message = ("%s has no available tests" % encoding)
            self.assertTrue(exists, message)
            with open(path, "rb") as stream:
                data = stream.read()
            guess = detector.detect(data, strict=False)
            if encoding != guess:
                wrong_guesses.append((encoding, guess))
        message = "List of misguesses:\n\t"
        message += "\n\t".join(
            "%s guessed as %s" % (enc,guess) for enc,guess in wrong_guesses
        )
        self.assertEqual(len(wrong_guesses), 0, message)

    def test_languages(self):
        """Try to create language objects."""
        wrong_guesses = []
        datatable = {
            # NOTE: Python as it seems does not have ArmSCII-8 encoding
            "hy"    : "\xb4\xb3\xf1\xbb\xf5 \xb3\xdf\xcb\xb3\xf1\xd1\\!",
            "ru"    : (u"\u041f\u0440\u0438\u0432\u0435\u0442, " +
                       u"\u043c\u0438\u0440!"),
            "ua"    : (u"\u041f\u0440\u0438\u0432\u0456\u0442, "
                       u"\u0441\u0432\u0456\u0442!"),
            "ja"    :  u"\u4e16\u754c\u3053\u3093\u306b\u3061\u306f\uff01",
            "zh-cn" :  u"\u4e16\u754c\uff0c\u4f60\u597d!",
            "zh-tw" :  u"\u4e16\u754c\uff0c\u4f60\u597d!",
            "tr"    :  u"Merhaba d\xfcnya!",
            "de"    :  u"Hallo, Welt!",
        }
        maxlen = len(max([str(core.Language(i)) for i in datatable], key=len))
        for language in datatable:
            data = datatable[language]
            language = core.Language(language)
            encoding = language.encodings[0]
            detector = core.Detector(language, [encoding])
            if isinstance(data, unicode):
                data = data.encode(encoding.mime)
            guess = detector.detect(data, strict=False)
            if encoding != guess:
                wrong_guesses.append((encoding, guess))
        message = "List of misguesses:\n\t"
        message += "\n\t".join(
            "%s guessed as %s" % (enc,guess) for enc,guess in wrong_guesses
        )
	self.assertEqual(len(wrong_guesses), 0, message)


if __name__ == "__main__":
    unittest.main()
