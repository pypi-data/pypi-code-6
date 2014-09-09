#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
import sys
import argparse


# if the amqp module wasn't yet installed at this system, load it from package
try:
    import edeposit.amqp.harvester as harvester
except (ImportError, AttributeError):
    sys.path.insert(0, os.path.abspath('../src/edeposit/amqp'))
    import harvester

from harvester.structures import Publications


# disable filtering for test purposes
harvester.settings.USE_DUP_FILTER = False
harvester.settings.USE_ALEPH_FILTER = False
reload(harvester.filters)


# Functions & objects =========================================================
def print_messages(pubs):
    """
    Print all publications from `pubs`.
    """
    for pub in pubs.publications:
        print pub
        print


# Main program ================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""This script is used to read data from
                       edeposit.amqp.harvester and print it to stdout."""
    )
    parser.add_argument(
        "-u",
        "--unittest",
        action="store_true",
        help="Perform unittest."
    )
    parser.add_argument(
        "-r",
        "--harvest",
        action="store_true",
        help="Harvest all data and send them to harvester queue."
    )
    parser.add_argument(
        "-d",
        "--dup-filter",
        action="store_true",
        help="Filter duplicate results. Default False."
    )
    args = parser.parse_args()

    if args.unittest:
        harvester.self_test()
    elif args.harvest or args.dup_filter:
        harvester.settings.USE_DUP_FILTER = args.dup_filter
        reload(harvester.filters)

        print_messages(
            Publications(harvester.get_all_publications())
        )
    else:
        parser.print_help()
