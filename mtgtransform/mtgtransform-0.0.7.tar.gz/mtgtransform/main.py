#!/usr/bin/env python
"""Magic deck transformer.

Transforms magic decks exported from mtgtop8.com into a format readable by
tappedout.net.

"""

import argparse
import sys
from . import transform


def main():
    parser = argparse.ArgumentParser(description='Transform magic deck.')
    parser.add_argument('inputfile', type=argparse.FileType('r'), nargs='?',
                        default=sys.stdin,
                        help='inputfile (default: stdin)')
    parser.add_argument('--sideboard', action='store_true',
                        help='Transform sideboard')

    args = parser.parse_args()
    data = args.inputfile.read()
    args.inputfile.close()
    print(transform(data, args.sideboard))

if __name__ == '__main__':
    sys.exit(main())
