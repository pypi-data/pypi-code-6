"""
This module acts as a drop-in replacement to some of Python's `os` module where the blocking operations are done in a
gevent-friendly manner.
"""
from __future__ import absolute_import
import os as _os
from gevent.fileobject import FileObject
from gevent.os import make_nonblocking, nb_read, nb_write

from .deferred import create_threadpool_executed_func

DEFERRED_FUNCTIONS = [
    'fchmod', 'fchown', 'fdatasync', 'fpathconf', 'fstat', 'fstatvfs', 'fsync', 'ftruncate',
    'access', 'chdir', 'fchdir', 'chflags', 'chmod', 'chown', 'lchflags', 'lchmod', 'lchown', 'link',
    'listdir', 'lstat', 'mkfifo', 'mknod', 'mkdir', 'makedirs', 'readlink', 'remove', 'removedirs',
    'rename', 'renames', 'rmdir', 'stat', 'stat_float_times', 'statvfs', 'symlink', 'tempnam',
    'tmpnam', 'unlink', 'utime'
]


__all__ = ['fopen', 'open', 'read', 'write'] + DEFERRED_FUNCTIONS


class _FileObjectWithContext(FileObject):
    """Adds context manager functionality to gevent's `FileObject`."""
    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


_fopen = create_threadpool_executed_func(open)


def fopen(name, mode='r', buffering=-1):
    """Similar to Python's built-in `open()` function."""
    f = _fopen(name, mode, buffering)
    return _FileObjectWithContext(f, mode, buffering)


_open = create_threadpool_executed_func(_os.open)


def open(file, flags, mode=0777):
    fd = _open(file, flags, mode)
    make_nonblocking(fd)
    return fd


read = nb_read
write = nb_write


# Here we convert most of os's file-related functions to functions that are deferred to a thread so they'll be
# gevent-friendly: they still will block, but will release the greenlet so other greenlets can execute.
module = globals()
for name in DEFERRED_FUNCTIONS:
    if name in _os.__dict__:
        module[name] = create_threadpool_executed_func(_os.__dict__[name])


# FIXME walk needs to be handled differently.
