#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module is used to make sure, that already processed books are removed from
queue.
"""
# Imports =====================================================================
import dup_filter
import aleph_filter

from .. import settings


# Functions & objects =========================================================
def filter_publication(publication):
    """
    Filter :class:`.Publication` objects using settings declared in
    :mod:`~harvester.settings` submodule.

    Args:
        publication (obj): :class:`.Publication` instance.

    Returns:
        obj/None: None if the publication was found in Aleph or `publication` \
                  if not.
    """
    if settings.USE_DUP_FILTER:
        publication = dup_filter.filter_publication(publication)

    if publication and settings.USE_ALEPH_FILTER:
        publication = aleph_filter.filter_publication(
            publication,
            cmp_authors=settings.ALEPH_FILTER_BY_AUTHOR
        )

    return publication


def filter_publications(publications):
    """
    Filter list of :class:`.Publication` objects.

    Args:
        publications (list): List of :class:`.Publication` instances.

    Returns:
        list: Correct objects.
    """
    return filter(lambda x: filter_publication(x), publications)
