#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

"""An immutable dictionary implementation."""

from collections import Mapping


class funcmap(Mapping):

    """Immutable dict for pure functional programming.

    This works basically like a regular dictionary, but doesn't mutate its
    state. All methods on funcmap which would normally mutate something return
    a new instance with the applied changes instead.

    """

    def __init__(self, it_or_map=tuple(), **kwargs):
        # NOTE: if a key is present in both it_or_map
        # and kwargs, the latter takes precedence.
        self.__storage = dict(it_or_map, **kwargs)

    @classmethod
    def new(cls, it_or_map=tuple(), **kwargs):
        return cls(it_or_map, **kwargs)

    def __getitem__(self, key):
        return self.__storage[key]

    def __iter__(self):
        return iter(self.__storage)

    def __len__(self):
        return len(self.__storage)

    def __repr__(self):
        return ("{" +
                ", ".join(["{}: {}".format(*map(repr, item))
                           for item in self.items()]) +
                "}")

    def set(self, key, value):

        def it():
            for i in self.items():
                yield i
            yield (key, value)

        return self.new(it())

    def remove(self, key):
        return self.new(
            [(k, v) for k, v in self.items() if k != key])
