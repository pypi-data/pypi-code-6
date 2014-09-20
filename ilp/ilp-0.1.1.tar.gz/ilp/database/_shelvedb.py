#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import shelve
from . import API


class ShelveDB(API):

    """A small wrapper around shelve.

    This database backend is meant mostly for testing and development purposes.

    """

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._shelve = shelve.open(self._path)

    def _put(self, key, value) -> None:
        self._shelve[key] = value

    def _get(self, key) -> "value":
        return self._shelve[key]

    def _del(self, key) -> None:
        del self._shelve[key]

    def __contains__(self, key) -> bool:
        return key in self._shelve
