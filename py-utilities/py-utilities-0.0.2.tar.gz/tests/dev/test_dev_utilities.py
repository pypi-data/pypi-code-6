#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py_utilities.dev.dev_utilities import deprecated
import unittest
import warnings


@deprecated()
def test_add_no_msg():
    return 1 + 1


@deprecated("Custom message, yo!")
def test_add_msg():
    return 1 + 1


class TestDev(unittest.TestCase):

    def test_deprecated(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            test_add_no_msg()
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Function 'test_add_no_msg' is deprecated." \
                in str(w[-1].message)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            test_add_msg()
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Custom message, yo!" in str(w[-1].message)

# vim: filetype=python
