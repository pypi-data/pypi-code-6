#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_romannumeral
----------------------------------

Tests for `romannumeral` module.
"""

import unittest

from romannumeral import RomanNumeral

from romannumeral import ParseError
from romannumeral import OutOfRangeError


class TestRomannumeral(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_roman_from_int(self):
        r = RomanNumeral(10)

        self.assertEqual(r.value, 10)
        self.assertEqual(r.string, 'X')

    def test_create_roman_from_str(self):
        r = RomanNumeral('X')

        self.assertEqual(r.value, 10)
        self.assertEqual(r.string, 'X')

    def test_create_roman_exhaustive(self):

        for n in range(10000):
            if n == 0 or n >= 4000:
                self.assertRaises(OutOfRangeError, RomanNumeral, n)
            else:
                r = RomanNumeral(n)
                self.assertEqual(r.value, n)

    def test_roman_from_badstring(self):
        """ Roman from malformed string should through parse exception """

        # no random sstring to roman
        self.assertRaises(ParseError, RomanNumeral, 'dfadsfafaf')

        # no string representation of number
        self.assertRaises(ParseError, RomanNumeral, '101')

        # no lower case
        self.assertRaises(ParseError, RomanNumeral, 'xviii')

        # no spaces
        self.assertRaises(ParseError, RomanNumeral, 'X V I I I')

    def test_roman_from_decimal(self):
        """ Roman from malformed string should through parse exception """
        self.assertRaises(ParseError, RomanNumeral, 3.14)

    def test_roman_from_negative(self):
        """ Roman below 0 throw an overflow exception """
        self.assertRaises(OutOfRangeError, RomanNumeral, -1)

    def test_roman_from_over_3999(self):
        """ Roman over 3999 throw an overflow exception """
        self.assertRaises(OutOfRangeError, RomanNumeral, 9001)

    def test_roman_addition(self):

        x = 2000
        for y in range(1, 4000):
            if 0 < x + y < 4000:
                roman_math = RomanNumeral(x) + RomanNumeral(y)
                self.assertEqual(roman_math, RomanNumeral(x + y))
            else:
                self.assertRaises(OutOfRangeError, RomanNumeral, x + y)

    def test_roman_subtraction(self):

        x = 2000
        for y in range(1, 4000):

            if 0 < x - y < 4000:
                roman_math = RomanNumeral(x) - RomanNumeral(y)
                self.assertEqual(roman_math, RomanNumeral(x - y))
            else:
                self.assertRaises(OutOfRangeError, RomanNumeral, x - y)

    def test_roman_multiplication(self):

        x = 10
        for y in range(1, 4000):

            if 0 < x * y < 4000:
                roman_math = RomanNumeral(x) * RomanNumeral(y)
                self.assertEqual(roman_math, RomanNumeral(x * y))
            else:
                self.assertRaises(OutOfRangeError, RomanNumeral, x * y)

    def test_roman_division(self):

        x = 3999
        for y in range(1, 4000):

            if 0 < x / y < 4000:
                roman_math = RomanNumeral(x) / RomanNumeral(y)
                self.assertEqual(roman_math, RomanNumeral(x // y))
            else:
                self.assertRaises(OutOfRangeError, RomanNumeral, x // y)

    def test_roman_exponent(self):

        x = 2
        for y in range(1, 60):

            if 0 < x ** y < 4000:
                roman_math = RomanNumeral(x) ** RomanNumeral(y)
                self.assertEqual(roman_math, RomanNumeral(x ** y))
            else:
                self.assertRaises(OutOfRangeError, RomanNumeral, x ** y)


if __name__ == '__main__':
    unittest.main()
