#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import os

from .utils import funcmap, funcset


class Index:

    """A collection of files and their associated tags.

    This object is immutable and changes no other state. All methods which
    would cause a state change return a new index object instead, with the
    changes applied.

    The index contains three major data structures:

        - a mapping of files to their content's hashes
        - a mapping of hashes to all filenames they identify
        - a mapping of all tags names to a set of the filenames they tag

    """

    files = property(lambda self: self._files)
    tags = property(lambda self: self._tags)
    hashes = property(lambda self: self._hashes)

    def __init__(self, files=None, tags=None, hashes=None):
        self._files = funcmap() if files is None else funcmap(files)
        self._tags = funcmap() if tags is None else funcmap(tags)
        self._hashes = funcmap() if hashes is None else funcmap(hashes)

    @classmethod
    def new(cls, files=None, tags=None, hashes=None):
        return cls(files, tags, hashes)

    def add_file(self, path, hashstring):
        """Add a new file to the index."""
        if path in self.files and self.files.get(path) != hashstring:
            raise ValueError(
                "Path exists in the database, but has a different hash.")
        new_files = self.files.set(path, hashstring)
        pathlist = self.hashes.get(hashstring, funcset())
        new_hashes = self.hashes.set(
            hashstring,
            pathlist.add(path))
        return self.new(new_files, self.tags, new_hashes)

    def remove_file(self, path):
        """Remove a path from the index.

        NOTE: Even if you remove the last duplicate of a file from the index,
        it will still store the hash, albeit with an empty list of paths
        associated with it.

        """
        if not path in self.files:
            raise KeyError("Path not in the index: {}".format(path))
        hashstring = self.files.get(path)
        new_files = self.files.remove(path)
        pathlist = self.hashes.get(hashstring, funcset())
        new_hashes = self.hashes.set(
            hashstring,
            pathlist.discard(path))
        return self.new(new_files, self.tags, new_hashes)

    def add_tag(self, name):
        """Add a new tag to the index.

        This method will silently return if the tag already exists.

        """
        if name in self.tags:
            raise KeyError("Tag already in the index: {}".format(name))
        return self.new(
            self.files,
            self.tags.set(name, funcset()),
            self.hashes)

    def remove_tag(self, name):
        """Remove a tag from the index."""
        if name not in self.tags:
            raise KeyError("Tag not in the index: {}".format(name))
        return self.new(
            self.files,
            self.tags.remove(name),
            self.hashes)

    def tag_file(self, path, tag_name):
        """Tag a file."""
        if tag_name not in self.tags:
            raise KeyError("Tag not in the index: {}".format(tag_name))
        if path not in self.files:
            raise KeyError("Path not in the index: {}".format(path))
        hashstring = self.files.get(path)
        new_tag = self.tags.get(tag_name).add(hashstring)
        return self.new(
            self.files,
            self.tags.set(tag_name, new_tag),
            self.hashes)

    def untag_file(self, path, tag_name):
        """Untag a file."""
        if tag_name not in self.tags:
            raise KeyError("Tag not in the index: {}".format(tag_name))
        if path not in self.files:
            raise KeyError("Path not in the index: {}".format(path))
        hashstring = self.files.get(path)
        new_tag = self.tags.get(tag_name).discard(hashstring)
        return self.new(
            self.files,
            self.tags.set(tag_name, new_tag),
            self.hashes)

    def file_has_tag(self, path, tag_name):
        """Check if a file is tagged by a tag."""
        if tag_name not in self.tags:
            # if the tag doesn't exist, no path can be tagged by it.
            return False
        tag = self.tags.get(tag_name)
        hashstring = self.files.get(path)
        return hashstring in tag

    def tags_of_file(self, path):
        """Return the names of all tags which are tagging a file."""
        hashstring = self.files.get(path)
        return funcset(tag_name
                       for tag_name, tag in self.tags.items()
                       if hashstring in tag)
