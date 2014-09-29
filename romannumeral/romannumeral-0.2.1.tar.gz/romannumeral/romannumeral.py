# -*- coding: utf-8 -*-

from .error import ParseError
from .error import OutOfRangeError
import re


ROMANS = (('M',  1000),
          ('CM', 900),
          ('D',  500),
          ('CD', 400),
          ('C',  100),
          ('XC', 90),
          ('L',  50),
          ('XL', 40),
          ('X',  10),
          ('IX', 9),
          ('V',  5),
          ('IV', 4),
          ('I',  1))

def parse_roman_numeral_from_string(s):

    roman_string = str(s)
    n = 0

    for letter, value in ROMANS:
        while letter == roman_string[:len(letter)]:
            n += value
            roman_string = roman_string[len(letter):]
    return n

def parse_roman_numeral_from_int(n):

    roman_int = int(n)
    s = ''

    for letter, value in ROMANS:
        while roman_int >= value:
            s += letter
            roman_int -= value
        if roman_int == 0:
            break
    return s


def validate_roman_string(s):
    """ Checks is a string matchs the proper syntax for a roman numeral

        Returs True if valid roman string else False

    """

    roman_pattern = '^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    return bool(re.match(roman_pattern, s)) and s.strip() != ''

class RomanNumeral(object):
    """ Represents an a Roman Numeral

    """

    def __init__(self, value):
        if isinstance(value, str):
            if not validate_roman_string(value):
                raise ParseError
            self.value = parse_roman_numeral_from_string(value)
            self.string = value
        elif isinstance(value, int):
            # roman numberals do not support 0 or values over 3999
            if not 0 < value < 4000:
                raise OutOfRangeError
            self.value = value
            self.string = parse_roman_numeral_from_int(value)
        else:
            raise ParseError

    def __repr__(self):
        return 'RomanNumeral({})'.format(self.value)


    def __str__(self):
        return self.string

    def __int__(self):
        return self.value


    def __lt__(self, value):
        return self.value < int(value)

    def __gt__(self, value):
        return self.value > int(value)

    def __eq__(self, value):
        return self.value == int(value)

    def __add__(self, other):
        return self.__class__(self.value + int(other))

    def __sub__(self, other):
        return self.__class__(self.value - int(other))

    def __mul__(self, other):
        return self.__class__(self.value * int(other))

    def __floordiv__(self, other):
        return self.__class__(self.value // int(other))

    def __mod__(self, other):
        return self.__class__(self.value % int(other))

    def __divmod__(self, other):
        return self.__floordiv__(other), self.__mod__(other)

    def __div__(self, other):
        return self.__floordiv__(other)

    def __truediv__(self, other):
        return self.__floordiv__(other)

    def __pow__(self, other, modulo=None):
        return self.__class__(self.value ** int(other))

    @classmethod
    def from_int(cls, roman_as_int):
        """ Create a RomanNumeral object from an int

        """

        cls(roman_as_int)

    @classmethod
    def from_string(cls, roman_as_string):
        """ Create a RomanNumeral object from an string

        """

        cls(roman_as_string)

