# -*- coding: utf-8 -*-

# isbntools - tools for extracting, cleaning and transforming ISBNs
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""isbntools main file.

Tools for extracting, cleaning, transforming and validating ISBN ids.
"""

import re
import logging

LOGGER = logging.getLogger(__name__)


RE_ISBN10 = re.compile(r'ISBN\x20(?=.{13}$)\d{1,5}([- ])\d{1,7}'
                       r'\1\d{1,6}\1(\d|X)$|[- 0-9X]{10,16}')
RE_ISBN13 = re.compile(r'97[89]{1}(?:-?\d){10,16}|97[89]{1}[- 0-9]{10,16}')
RE_STRICT = re.compile(r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|'
                       r'(?=(?:[0-9]+[- ]){3})'
                       r'[- 0-9X]{13}$|97[89][0-9]{10}$|'
                       r'(?=(?:[0-9]+[- ]){4})'
                       r'[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}'
                       r'[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
                       re.I | re.M | re.S)
RE_NORMAL = re.compile(r'97[89]{1}(?:-?\d){10}|\d{9}[0-9X]{1}|'
                       r'[-0-9X]{10,16}',
                       re.I | re.M | re.S)
RE_LOOSE = re.compile(r'[- 0-9X]{10,16}', re.I | re.M | re.S)
ISBN13_PREFIX = '978'
LEGAL = '0123456789xXisbnISBN- '


def _check_digit10(firstninedigits):
    """Check sum ISBN-10."""
    # minimum checks
    if len(firstninedigits) != 9:
        return None
    try:
        int(firstninedigits)
    except:  # pragma: no cover
        return None
    # checksum
    val = sum((i + 2) * int(x) for
              i, x in enumerate(reversed(firstninedigits)))
    remainder = int(val % 11)
    if remainder == 0:
        tenthdigit = 0
    else:
        tenthdigit = 11 - remainder
    if tenthdigit == 10:
        tenthdigit = 'X'
    return str(tenthdigit)


def _check_digit13(firsttwelvedigits):
    """Check sum ISBN-13."""
    # minimum checks
    if len(firsttwelvedigits) != 12:
        return None
    try:
        int(firsttwelvedigits)
    except:  # pragma: no cover
        return None
    # checksum
    val = sum((i % 2 * 2 + 1) * int(x) for
              i, x in enumerate(firsttwelvedigits))
    thirteenthdigit = 10 - int(val % 10)
    if thirteenthdigit == 10:
        thirteenthdigit = '0'
    return str(thirteenthdigit)


def _check_structure10(isbn10like):
    """Check structure of an ISBN-10."""
    return True if re.match(RE_ISBN10, isbn10like) else False


def _check_structure13(isbn13like):
    """Check structure of an ISBN-13."""
    return True if re.match(RE_ISBN13, isbn13like) else False


def is_isbn10(isbn10):
    """Validate as ISBN-10."""
    isbn10 = canonical(isbn10)
    if len(isbn10) != 10:
        return False          # pragma: no cover
    else:
        return False if _check_digit10(isbn10[:-1]) != isbn10[-1] else True


def is_isbn13(isbn13):
    """Validate as ISBN-13."""
    isbn13 = canonical(isbn13)
    if len(isbn13) != 13:
        return False          # pragma: no cover
    else:
        return False if _check_digit13(isbn13[:-1]) != isbn13[-1] else True


def to_isbn10(isbn13):
    """Transform isbn-13 to isbn-10."""
    # Check prefix
    if isbn13[:3] != ISBN13_PREFIX:
        return None
    isbn10 = isbn13[3:]
    check = _check_digit10(isbn10[:-1])
    # Change check digit
    return isbn10[:-1] + check if check else None


def to_isbn13(isbn10):
    """Transform isbn-10 to isbn-13."""
    isbn13 = ISBN13_PREFIX + isbn10[:-1]
    check = _check_digit13(isbn13)
    return isbn13 + check if check else None


def canonical(isbnlike):
    """Keep only numbers and X."""
    numb = [c for c in isbnlike if c in '0123456789X']
    return ''.join(numb)


def clean(isbnlike):
    """Clean ISBN (only legal characters)."""
    cisbn = [c for c in isbnlike if c in LEGAL]
    buf = re.sub(r'\s*-\s*', '-', ''.join(cisbn))
    return re.sub(r'\s+', ' ', buf).strip()


def notisbn(isbnlike, level='strict'):
    """Check with the goal to invalidate isbn-like.

    level:
    strict for certain they are not ISBNs (default)
    loose  only filters obvious NO ISBNs

    """
    if level not in ('strict', 'loose'):
        LOGGER.error('level as no option %s', level)
        return
    isbnlike = canonical(isbnlike)
    if len(isbnlike) not in (10, 13):
        return True
    if level != 'strict':
        return False
    if len(isbnlike) == 10:
        # an isbn-10 starting with 94 is not valid
        return True if isbnlike[0:2] == '94' else not is_isbn10(isbnlike)
    else:
        return True if isbnlike[3:5] == '94' else not is_isbn13(isbnlike)


def get_isbnlike(text, level='normal'):
    """Extract all substrings that seem like ISBNs.

    level:
    strict almost as certain they are ISBNs
    normal (default)
    loose  catch many as possible

    """
    if level == 'normal':
        isbnlike = RE_NORMAL
    elif level == 'strict':
        isbnlike = RE_STRICT
    elif level == 'loose':
        isbnlike = RE_LOOSE
    else:
        LOGGER.error('level as no option %s', level)
        return
    return isbnlike.findall(text)


def get_canonical_isbn(isbnlike, output='bouth'):
    """Extract ISBNs and transform them to the canonical form.

    output:
    isbn10
    isbn13
    bouth  (default)

    """
    if output not in ('bouth', 'isbn10', 'isbn13'):
        LOGGER.error('output as no option %s', output)
        return

    regex = RE_NORMAL

    match = regex.search(isbnlike)
    if match:
        # Get only canonical characters and split them into a list
        cisbn = canonical(match.group())
        chars = list(cisbn)
        # Remove the last digit from `chars` and assign it to `last`
        last = chars.pop()
        buf = ''.join(chars)

        if len(chars) == 9:
            # Compute the ISBN-10 checksum digit
            check = _check_digit10(buf)
        else:
            # Compute the ISBN-13 checksum digit
            check = _check_digit13(buf)

        # If checksum OK return a `canonical` ISBN
        if str(check) == last:
            if output == 'bouth':
                return cisbn
            if output == 'isbn10':
                return cisbn if len(cisbn) == 10 else to_isbn10(cisbn)
            return to_isbn13(cisbn) if len(cisbn) == 10 else cisbn


def EAN13(isbnlike):
    """Transform an `isbnlike` string in an EAN number (canonical ISBN-13)."""
    ib = canonical(isbnlike)
    if len(ib) == 13:
        return ib if is_isbn13(ib) else None
    elif len(ib) == 10:
        return to_isbn13(ib) if is_isbn10(ib) else None
