#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kirschwasser - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

"""database - the storage backend API."""

from abc import ABCMeta, abstractmethod


class DatabaseAPI(metaclass=ABCMeta):

    """Abstract metaclass for all database APIs.

    Subclasses must implement _put, _get, _del, and __contains__.

    Note that the first three shouldn't generally check for key existence, the
    user facing methods (store, update, retrieve, remove) do that.

    """

    @abstractmethod
    def _put(self, key, value) -> None:
        return NotImplemented

    @abstractmethod
    def _get(self, key) -> "value":
        return NotImplemented

    @abstractmethod
    def _del(self, key) -> None:
        return NotImplemented

    @abstractmethod
    def __contains__(self, key) -> bool:
        return NotImplemented

    def store(self, key, value):
        """Store an item in the database.

        This method refuses to change existing values. Use update() for that.

        """
        if key in self:
            raise KeyError("'{}' already exists.".format(key))
        self._put(key, value)

    def update(self, key, value, create=False):
        """Change an existing key in the database.

        By default, this method will raise a KeyError if the key doesn't
        already exist. Set create=True if you want it to create a new key.

        """
        if key not in self and not create:
            raise KeyError("'{}' doesn't exist.".format(key))
        else:
            self._put(key, value)

    def retrieve(self, key):
        """Retrieve a key from the database."""
        if key not in self:
            raise KeyError("'{}' doesn't exist.".format(key))
        return self._get(key)

    def remove(self, key):
        """Delete a key from the database."""
        if key not in self:
            raise KeyError("'{}' doesn't exist.".format(key))
        self._del(key)
