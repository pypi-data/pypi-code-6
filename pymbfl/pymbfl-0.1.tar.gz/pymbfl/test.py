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
_LOGGER = logging.getLogger(__file__)
_LOGGER.setLevel(logging.DEBUG)
_HANDLER = logging.StreamHandler(stream=sys.stderr)
_FORMATTER = logging.Formatter("%(message)s")
_HANDLER.setFormatter(_FORMATTER)
_LOGGER.addHandler(_HANDLER)


class TestPyMBFL(unittest.TestCase):
    """Run PyMBFL testing suite."""

    def test_encodings(self):
        """Try to iterate through names of multi-byte encodings."""
        for encoding in const.ENCODINGS:
            encoding = core.Encoding(encoding)

    def test_detector(self):
        """Check all available multi-byte detectors."""
        maxlen = max([len(str(i)) for i in const.ENCODINGS])
        for encoding in [core.Encoding(i) for i in const.ENCODINGS]:
            exists = False
            detector = core.Detector(language="", encodings=[encoding])
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
            guess = detector.detect(data, strict=True)
            if encoding == guess:
                _LOGGER.info("%%-%ds SUCCESS" % maxlen % encoding)
            else:
                _LOGGER.info("%%-%ds FAILURE " % maxlen % encoding)
            #message = ("%s was not determined" % encoding)
            #self.assertEqual(encoding, guess, message)

    def test_languages(self):
        """Try to create language objects."""
        languages = ["ru", "ko", "en", "neutral"]
        maxlen = len(max(languages, key=len))
        for language in languages:
            language = core.Language(language)
            _LOGGER.info(repr(language))
            _LOGGER.info("\t" + repr(language.encodings))


if __name__ == "__main__":
    unittest.main()
