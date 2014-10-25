"""The version module for this package.

Whenever this module is imported, it will always attempt to update its
version string by fetching a new one from the VCS.  If that fails then
it retains the one that's already saved to its cache file.  The cache
file is the current module's _version module (_version.py).

Currently, only git is a supported VCS.

"""

# Copyright (C) 2014 Kieran Colford

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

import os
import re
import subprocess
import sys


def getDir():
    """Return the directory that this file is in."""

    thisfile = sys.modules[__name__].__file__
    thisdir = os.path.dirname(thisfile)

    return thisdir


def callGit(args):
    """Call git with args and return the output."""

    return subprocess.check_output(['git', '-C', getDir()] + args,
                                   stderr=subprocess.STDOUT)


def acceptsIgnoreRule(path):
    """Return whether the file at path will accept the ignore rule."""

    with open(path) as f:
        rules = set(f.readlines())
    return '/_version.py\n' not in rules


def updateCache(ver):
    """Update the cache file with the version string ver."""

    # Make sure the ignore file is in place so that our generated file
    # is ignored by VCS.
    ignorepath = os.path.join(getDir(), '.gitignore')

    if os.path.exists(ignorepath) and acceptsIgnoreRule(ignorepath):
        # ignorepath is already there, and it doesn't have a rule that
        # ignores _version.py.
        with open(ignorepath, 'a') as f:
            f.write('/_version.py\n')
    else:
        # ignorepath doesn't exist yet so we have to create it.
        with open(ignorepath, 'w') as f:
            f.write('/_version.py\n' + '/.gitignore\n')

    # Generate the cache module.
    cachepath = os.path.join(getDir(), '_version.py')
    with open(cachepath, 'w') as f:
        f.write('version = ' + repr(ver))


def getVersion():
    """Return the version string.

    We'll update the _version.py file found in the package if we can.
    This is where the version string is cached in case the package is
    distributed outside of of a git repository.

    """

    try:
        ver = callGit(['describe', '--tags', '--abbrev=3', '--match=v*'])
        ver = ver.strip('v\n')
        ver = ver.replace('-', '.', 1)
        ver = ver.split('-')[0]
        updateCache(ver)
    except OSError, CalledProcessError:
        import _version
        ver = _version.version

    return ver

# Comment/Uncomment this to show/hide the function definitions above.
# This is useful if the package doesn't want to show the internals of
# its version generation or if a developer wants to read the module in
# pydoc.
__all__ = ['version']

version = getVersion()
