#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import os
import shlex

from distutils.util import strtobool

import plac

from .. import database
from ..utils import file
from ..utils import funcset

from ..index import Index


class ILP:

    """A tag based file indexer."""

    commands = (
        "index",
        "forget",
        "tag",
        "untag",
        "deltag",
        "list",
        "info",
        "search",
        "clear")

    def __init__(self):
        home = os.getenv("HOME")
        self._confdir = os.path.join(home, ".ilp")
        if not file.exists(self._confdir):
            os.mkdir(self._confdir)
        self._dbfile = os.path.join(self._confdir, "database")
        self._index = Index()

    def __enter__(self):
        self._database = database.ShelveDB(self._dbfile)
        if "index" in self._database:
            self._index = self._database.retrieve("index")
        else:
            self._index = Index()
            self._database.store("index", self._index)
        return self

    def __exit__(self, etype, exc, tb):
        self._database.update("index", self._index)
        #self._database.close()
        pass

    def index(self,
              recursive: ("recursively add files below a given directory",
                          "flag",
                          "r"),
              *paths: "files or directories to add to the index"):
        for path in paths:
            if file.isdir(path):
                if not recursive:
                    yield "Is a directory: {}".format(path)
                    yield "(To recursively add files to the index, pass -r)"
                else:
                    for subpath in file.walk(path):
                        for output in self.index(False, subpath):
                            yield output
                continue
            full_path = os.path.abspath(path)
            hashstring = None
            try:
                hashstring = file.hash(full_path)
            except Exception as e:
                yield "Couldn't read file: {}".format(full_path, e)
                continue
            self._index = self._index.add_file(full_path, hashstring)
            yield "Adding to the index: {}".format(path)

    def forget(self,
               recursive: ("recursively remove files below a given directory",
                           "flag",
                           "r"),
               *paths: "files or directories to remove from the index"):
        for path in paths:
            if file.isdir(path):
                if not recursive:
                    yield "Is a directory: {}".format(path)
                    yield "(To recursively remove files from the index, pass -r)"
                else:
                    for subpath in file.walk(path):
                        for output in self.forget(False, subpath):
                            yield output
                continue
            full_path = os.path.abspath(path)
            if full_path in self._index.files:
                self._index = self._index.remove_file(full_path)
                yield "Removing from the index: {}".format(path)
            else:
                yield "{} doesn't exist in the index.".format(path)

    def tag(self,
            path: "file or directory to apply tags to",
            recursive: ("recursively add tags to all files below a given directory",
                        "flag",
                        "r"),
            *tags: "tags to add to the file or directory"):
        full_path = os.path.abspath(path)
        if file.isdir(full_path):
            if recursive:
                for subpath in file.walk(path):
                    for output in self.tag(subpath, False, *tags):
                        yield output
            else:
                yield "Is a directory: {}".format(path)
                yield "(To recursively tag files in a directory, pass -r)"
        else:
            for tag_name in tags:
                if not tag_name in self._index.tags:
                    self._index = self._index.add_tag(tag_name)
                    yield "New tag added: {}".format(tag_name)
                if not self._index.file_has_tag(full_path, tag_name):
                    self._index = self._index.tag_file(full_path, tag_name)
                    yield "{} → {}".format(tag_name, path)
                else:
                    yield "{} is already tagging {}".format(tag_name, path)

    def untag(self,
            path: "file or directory to remove tags from",
            recursive: ("recursively remove tags from all files below a given directory",
                        "flag",
                        "r"),
            *tags: "tags to remove from the file or directory"):
        full_path = os.path.abspath(path)
        if file.isdir(full_path):
            if recursive:
                for subpath in file.walk(path):
                    for output in self.untag(subpath, False, *tags):
                        yield output
            else:
                yield "Is a directory: {}".format(path)
                yield "(To recursively untag files in a directory, pass -r)"
        else:
            for tag_name in tags:
                if not tag_name in self._index.tags:
                    yield "Tag doesn't exist: {}".format(tag_name)
                if self._index.file_has_tag(full_path, tag_name):
                    self._index = self._index.untag_file(full_path, tag_name)
                    yield "Removed {} from {}".format(tag_name, path)
                else:
                    yield "{} isn't tagging {}".format(tag_name, path)

    def deltag(self,
               *tag_names: "tags to delete"):
        for tag_name in tag_names:
            if not tag_name in self._index.tags:
                yield "Tag not in the index: {}".format(tag_name)
            else:
                self._index = self._index.remove_tag(tag_name)
                yield "Deleted {}".format(tag_name)

    def list(self,
             what: ("items to list",
                    "positional",
                    None,
                    None,
                    ("files", "tags"),
                    None)):
        if what == "files":
            for path in self._index.files:
                yield path
        elif what == "tags":
            for tag_name in self._index.tags:
                yield tag_name
        else:
            yield "Can't list {}.".format(what)

    def info(self,
             item: "file or tag to get information about",
             tag: ("get information on tags",
                      "flag",
                      "t")):
        # for better code readability and less accidental collisions
        is_tag = tag
        # get all tags tagging the given path
        if not is_tag:
            path = item
            full_path = os.path.abspath(path)
            if not full_path in self._index.files:
                yield "File not in the index: {}".format(path)
            else:
                for tag_name in self._index.tags_of_file(full_path):
                    yield(tag_name)
        # get all paths this tag is tagging
        else:
            tag_name = item
            if not tag_name in self._index.tags:
                yield "Tag not in the index: {}".format(tag_name)
            else:
                tag = self._index.tags.get(tag_name)
                for hashstring in tag:
                    for path in self._index.hashes.get(hashstring):
                        yield(path)

    def search(self,
               query: "the search query"):
        split = shlex.split(query)
        result = self._build_search_result(
            funcset(self._index.hashes), "or", split)
        for hashstring in result:
            try:
                for path in self._index.hashes.get(hashstring):
                    yield path
            except KeyError:
                yield "Unknown hash: {}".format(hashstring)

    def _build_search_result(self, result, operator, tail):
        if len(tail) == 0:
            return result
        else:
            item, tail = tail[0], tail[1:]
            if item in ("and", "or", "not", "xor"):
                operator = item
                return self._build_search_result(result, operator, tail)
            else:
                if item not in self._index.tags:
                    raise KeyError("Tag not in index: {}".format(item))
                operation = {
                    "or": result.__or__,
                    "and": result.__and__,
                    "not": result.__sub__,
                    "xor": result.__xor__}[operator]
                tag = self._index.tags.get(item)
                result = operation(tag)
                return self._build_search_result(result, operator, tail)

    def clear(self,
              yes: ("Confirm deletion",
                    "flag",
                    "y")):
        """Clear the database."""
        if not yes:
            yield "This command purges the database."
            yield "You will LOSE ALL DATA!"
            yield "If you really want this, pass -y to this command."
        else:
            yield "Purging the database."
            self._index = Index()


def main():
    plac.Interpreter.call(ILP, prompt="ilp> ")

if __name__ == "__main__":
    main()
