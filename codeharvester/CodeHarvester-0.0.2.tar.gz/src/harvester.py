#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# CodeHarvester - harvester.py (runner)
#
# Copyright (c) 2014 Denis Gonsiorovsky
# Licensed under the MIT license

import argparse
from codeharvester.harvester import VERSION, JSHarvester


def version():
    print("CodeHarvester {0}".format(VERSION))


def main():
    parser = argparse.ArgumentParser(description='Merge an input file and all of its requirements into a single file.')
    parser.add_argument('input', metavar='INPUT', type=str,
                       help='process INPUT file')
    parser.add_argument('--version', action='store_true',
                        help='show program version and exit')
    parser.add_argument('-o', '--output', type=str,
                        help='write document to OUTPUT (defaults to STDOUT)')
    parser.add_argument('--verbose', action='store_true',
                        help='use verbose output')
    parser.add_argument('--no-cleanup', dest='cleanup', action='store_false',
                        help='don\'t cleanup incorrect statements in the output')

    parser.set_defaults(version=False)
    parser.set_defaults(verbose=False)
    parser.set_defaults(cleanup=True)

    args = parser.parse_args()

    if args.version:
        version()
        exit(0)

    h = JSHarvester(flags={
        'verbose': args.verbose,
        'cleanup': args.cleanup
    })
    h.harvest_file(args.input, args.output)

if __name__ == "__main__":
    main()