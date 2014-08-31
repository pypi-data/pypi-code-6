#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utl - python's unittest lister.

    A simple tool that shows available tests without executing them.

Usage:
    utl ENTRY_POINT

Arguments:
    ENTRY_POINT    path to dir where scanning is up to begin

Options:
    -h --help       Show this screen.
    -v --version    Show version.
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from docopt import docopt
from utl import __version__


def suite2testname(suite):
    description = str(suite)
    test_name, raw_test_head = description.split()
    test_head = raw_test_head[1:-1]
    test_path = '.'.join([test_head, test_name])
    return test_path


def print_suite(suite, indent):
    if hasattr(suite, '__iter__'):
        for x in suite:
            print_suite(x, indent)
    else:
        test_name = suite2testname(suite)
        print(indent + test_name)


def main():
    arguments = docopt(__doc__, version=__version__)
    entry_point = arguments.get('ENTRY_POINT')
    print_suite(unittest.defaultTestLoader.discover(entry_point), '')


if __name__ == '__main__':
    main()
