#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

"""An immutable set implementation."""

from collections import Set


class funcset(Set):

    """Immutable set for pure functional programming.

    funcset implements some methods of a regular, mutable set (add, discard,
    remove), but instead of mutating itself, it will always return either a new
    instance of itself with the changes, or itself if nothing changed.

    """

    def __init__(self, it=tuple()):
        self.__storage = frozenset(it)

    @classmethod
    def new(cls, it=tuple()):
        return cls(it)

    def __contains__(self, x):
        return x in self.__storage

    def __iter__(self):
        return iter(self.__storage)

    def __len__(self):
        return len(self.__storage)

    def __repr__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def add(self, item):
        if item in self:
            return self
        return self | (item,)

    def discard(self, item):
        if item not in self:
            return self
        return self - (item,)

    def remove(self, item):
        if item not in self:
            raise KeyError(item)
        return self.discard(item)
