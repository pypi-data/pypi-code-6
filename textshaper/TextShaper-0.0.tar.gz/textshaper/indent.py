#!/usr/bin/env python

"""
indentation of text blocks
"""

import argparse
import os
import sys
from .decorator import lines

@lines
def indent(text, indentation=4, space=' ', strict=False):
    """
    indent a block of text

    text -- lines of text to indent
    indentation -- number of spaces to indent
    space -- what to indent with
    strict -- whether to enforce required whitespace for negative indentation
    """

    if not indentation:
        # nothing to do
        return text

    if indentation > 0:
        retval = [space * indentation + line for line in text]
    else:
        # negative indentation
        indentation = -indentation
        retval = []
        for line in text:
            prefix = line[:indentation]
            for index, char in enumerate(prefix):
                if not char == space:
                    if strict:
                        raise AssertionError("Found non-'%s' charcter at column %d for indentation -%d" % (space, index, indentation))
                    break
            else:
                index = indentation
            retval.append(line[index:])

    return retval

@lines
def deindent(text):
    """strip lines"""
    return [line.strip() for line in text]

### CLI

def add_arguments(parser):
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('-o', '--output', dest='output',
                        help="output file or stdout if not given")


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    description = """indent files or stdin if no files given"""
    parser = argparse.Argument(description=__doc__)
    add_arguments(parser)
    options = parser.parse_args(args)

    # process input
    for f in _files():

        # indent the text
        indented = '\n'.join(indent(f))

        # append to output
        if options.output:
            with open(options.output, 'a') as f:
                f.write(indented)
        else:
            sys.stdout.write(indented)

if __name__ == '__main__':
    main()
