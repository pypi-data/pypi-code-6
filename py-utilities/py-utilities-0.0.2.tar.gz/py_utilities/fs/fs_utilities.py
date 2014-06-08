#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..decorators import safe
import errno
import os
import shutil


def mkdir_p(path):
    """
    Recursive directory creation function. Mimics `mkdir -p`. Doesn't
    raise an error if the leaf exists and is a directory.

    Reference: http://stackoverflow.com/questions/600268/\
    mkdir-p-functionality-in-python/600612#600612
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_if_exists(path):
    """
    Removes a file silently
    """
    try:
        os.remove(path)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise


def rm_rf(path, ignore_errors=True):
    """
    Recursive directory deletion function.
    """
    shutil.rmtree(path, ignore_errors=ignore_errors)


@safe(lambda path: os.stat(path), (os.error,))
def safe_stat(path):
    """
    Return stat system call (without raising an ``os.error``)
    """
    pass  # pragma: no cover


def touch(path, times=None):
    """
    Touches a file. If times is None, then the file’s access and modified
    times are set to the current time.
    """
    with file(path, 'a'):
        os.utime(path, times)

# vim: filetype=python
