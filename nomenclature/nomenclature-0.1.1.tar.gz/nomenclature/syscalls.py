# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
Syscalls to manipulate linux namespaces.
"""

import os

from ._lib import lib, ffi

def _check_error(errno):
    if errno != 0:
        raise OSError(errno, os.strerror(errno))

def unshare(flags):
    """
    Disassociate parts of the process execution context.

    :param flags int: A bitmask that specifies which parts of the execution
        context should be unshared.
    """
    res = lib.unshare(flags)
    if res != 0:
        _check_error(ffi.errno)


def setns(fd, nstype):
    """
    Reassociate thread with a namespace

    :param fd int: The file descriptor referreing to one of the namespace
        entries in a :directory::`/proc/<pid>/ns/` directory.
    :param nstype int: The type of namespace the calling thread should be
        reasscoiated with.
    """
    res = lib.setns(fd, nstype)
    if res != 0:
        _check_error(ffi.errno)
        

for var in dir(lib):
    if var.startswith('CLONE_'):
        globals()[var] = getattr(lib, var)
