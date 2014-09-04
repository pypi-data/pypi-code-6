#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
quote some lines
"""

import argparse
import os
import sys

def quotelines(text, quote="'", close_quote=None):
    """
    individually quote each line of text

    quote -- quote character to use
    close_quote -- closing quote character, if different from opening quote
    """

    close_quote = quote if close_quote is None else close_quote
    return ["{}{}{}".format(quote, line, close_quote) for line in lines]


def main(args=sys.argv[1:]):
    """CLI"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input file, or read from stdin if ommitted')
    options = parser.parse_args(args)

    lines = quotelines(options.input)

    print '\n'.join(lines)

if __name__ == '__main__':
    main()
