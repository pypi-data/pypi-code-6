#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import filters
import scrappers
from scrappers import ben_cz
from scrappers import grada_cz
from scrappers import cpress_cz
from scrappers import zonerpress_cz


# Functions & objects =========================================================
def get_all_publications(return_namedtuples=True):
    """
    Get list publications from all available source.

    Args:
        return_namedtuples (bool, default True): Convert :class:`.Publication`
                           structures to namedtuples (used in AMQP
                           communication).

    Returns:
        list: List of :class:`.Publication` structures converted to namedtuple.
    """
    sources = [
        ben_cz.get_publications,
        grada_cz.get_publications,
        cpress_cz.get_publications,
        zonerpress_cz.get_publications,
    ]

    # get data from all scrappers
    publications = []
    for source in sources:
        publications.extend(
            filters.filter_publications(source())
        )

    # convert to namedtuples
    if return_namedtuples:
        publications = map(lambda x: x.to_namedtuple(), publications)

    return publications


def self_test():
    """
    Perform selftest.

    Returns:
        None: None if everything is ok.

    Raises:
        UserWarning: If one of the tests fails.
    """
    ben_cz.self_test()
    grada_cz.self_test()
    cpress_cz.self_test()
    zonerpress_cz.self_test()
