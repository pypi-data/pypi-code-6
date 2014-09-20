#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

"""An interface to files on the disk.

Since this module deals with touching the disk, all functions it provides
should be considered impure unless noted otherwise.

Pure functions in this module:
    - filter (fnmatch.filter, provided for convenience)
    - hash_bytes (a small wrapper function around hashlib's algorithms)

"""

# Since these modules aren't part of the public API of this module, we import
# them under different names to hide them.
import hashlib as _hashlib
import os as _os
import itertools as _itertools

# for convenience
from os.path import exists, isdir

# NOTE: This overwrites builtins.filter in this module. Should it be needed in
# the future, either ``import builtins'' or store it somewhere before importing
# (e.g. ``_filter'').
from fnmatch import filter


def is_readable(path: str) -> bool:
    """Test whether a file is readable."""
    try:
        with open(path):
            pass
    except:  # we consider any error as the file not being readable
        return False
    return True


def read(path: str) -> bytes:
    """Try to read a file from disk.

    Note that this function assumes that the caller has checked for
    preconditions such as existence and readability of the file, or
    is prepared to handle any exceptions that might occur.

    """
    with open(path, "rb") as f:
        return f.read()


def hash_bytes(bytestream: bytes, hashfunc=_hashlib.sha1) -> bytes:
    """Hash a stream of bytes. Defaults to using sha1.

    To use a different hashing algorithm, pass any of the functions from hashlib
    as a second argument (or anything that conforms to the same interface). For
    example, to use md5:

        import hashlib
        hash_bytes(b'some bytes', hashlib.md5)

    This is a pure function.

    """
    return hashfunc(bytestream).digest()


def hash(path: str, hashfunc=_hashlib.sha1) -> bytes:
    """Read and hash a file's contents."""
    contents = read(path)
    return hash_bytes(contents, hashfunc)


def walk(path: str) -> [str]:
    """Get a list of all non-directory files below the given path."""

    def join(dirname, filenames):
        return [_os.path.join(dirname, filename) for filename in filenames]

    # We don't care for the dirnames part of os.walk, which is the middle part
    # of the tuples it generates.
    return _itertools.chain(
        *[join(dirname, filenames)
          for dirname, _, filenames in _os.walk(path)])


def find(path: str, pattern: str) -> [str]:
    """Recursively find all files below path matching the glob pattern."""
    return filter(walk(path), pattern)
