# Copyright (C) 2014 Kieran Colford
#
# This file is part of txt2boil.
#
# txt2boil is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# txt2boil is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with txt2boil.  If not, see <http://www.gnu.org/licenses/>.

"""The version module for this package.

Whenever this module is imported, it will always attempt to update its
version string by fetching a new one from the VCS.  If that fails then
it retains the one that's already saved to its cache file.  The cache
file is the current module's _version module (_version.py).

Currently, only git is a supported VCS.

"""

import os
import re
import subprocess
from subprocess import CalledProcessError
import sys


def getDir():
    """Return the directory that this file is in."""

    thisfile = sys.modules[__name__].__file__
    thisdir = os.path.dirname(thisfile)

    return thisdir


def callGit(args):
    """Call git with args and return the output."""

    out = subprocess.check_output(['git', '-C', getDir()] + args,
                                  stderr=subprocess.STDOUT)
    return str(out)


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
        ver = callGit(['describe', '--match=v*'])
        ver = ver.strip('v\n')
        ver = ver.replace('-', '.', 1)
        ver = ver.split('-')[0]
        updateCache(ver)
    except OSError:
        import _version
        ver = _version.version
    except CalledProcessError:
        import _version
        ver = _version.version

    return ver

# Comment/Uncomment this to show/hide the function definitions above.
# This is useful if the package doesn't want to show the internals of
# its version generation or if a developer wants to read the module in
# pydoc.
__all__ = ['version']

version = getVersion()
