#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This submodule is used to skip already parsed data.

Each `publication` parameter of the :func:`filter` is cached and if it is
called with same parameter again, None is retuned.

Note:
    Cache is using simple JSON serialization, so some form of cache persistency
    is granted. For path to the serialized data, look at
    :attr:`~harvester.settings.DUP_FILTER_FILE`.
"""
# Imports =====================================================================
import json
import os.path

from .. import settings


# Variables ===================================================================
_CACHE = None


# Functions & objects =========================================================
def save_cache(cache):
    """
    Save cahce to the disk.

    Args:
        cache (set): Set with cached data.
    """
    with open(settings.DUP_FILTER_FILE, "w") as f:
        f.write(
            json.dumps(list(cache))
        )


def load_cache():
    """
    Load cache from the disk.

    Return:
        set: Deserialized data from disk.
    """
    if not os.path.exists(settings.DUP_FILTER_FILE):
        return set()

    with open(settings.DUP_FILTER_FILE) as f:
        return set(
            json.loads(f.read())
        )


def filter_publication(publication, cache=_CACHE):
    """
    Deduplication function, which compares `publication` with samples stored in
    `cache`. If the match NOT is found, `publication` is returned, else None.

    Args:
        publication (obj): :class:`.Publication` instance.
        cache (obj): Cache which is used for lookups.

    Returns:
        obj/None: Depends whether the object is found in cache or not.
    """
    if cache is None:
        cache = load_cache()

    if publication._get_hash() in cache:
        return None

    cache.update(
        [publication._get_hash()]
    )
    save_cache(cache)
    return publication
