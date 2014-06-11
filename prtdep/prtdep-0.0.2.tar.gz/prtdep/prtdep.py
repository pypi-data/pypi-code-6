#!/usr/bin/env python
# Author: Darko Poljak <darko.poljak@gmail.com>
# License: GPLv3

"""{0} {1}

Usage: {0} [options] <ports-root-path>...

Arguments:
    <ports-root-path> ports root directory path

    Options:
        -h, --help                     show this screen
        -v, --version                  show version and exit
        -p, --dump                     dump all dependencies and all dependents
                                       for each package
        -s, --dump-deps                dump all dependencies for each package
        -e, --dump-dept                dump all dependent packages for each package
        -o, --orphans                  print orphans
        -i <pkgs>, --get-deps=<pkgs>   get dependencies for comma separated
                                       package list
        -t <pkgs>, --get-dept=<pkgs>   get dependent packages for comma separated
                                       package list
        -r <pkgs>, --remove=<pkgs>     remove comma separated package list,
                                       in specified order
        -a, --after                    do info printing after removing
        -b, --before                   do info printing before removing (default)
        """

from __future__ import print_function

__author__ = 'Darko Poljak <darko.poljak@gmail.com>'
__version__ = '0.0.2'
__license__ = 'GPLv3'

__all__ = [
    'Prtdep', 'PrtdepException'
]

import os
from os.path import join
from collections import defaultdict, deque
import re


class PrtdepException(Exception):
    pass


class Prtdep(object):
    '''
    Help resolving dependencies for CURX ports.
    It calculates dependencies for specified list of ports root paths.
    It can list dependencies for list of packages, list packages that
    depend on specified list of packages. For specified packages it
    can print list of packages that can freely be removed after them
    to have system without orphans.
    '''

    PKG_FILE_NAME = 'Pkgfile'
    # one group for name
    PKG_NAME_REGEX = r'^name=([^\s]+)\s*$'
    # one group for depends on list
    PKG_DEPENDS_ON_REGEX = r'^.*Depends on:\s*(.*)\s*$'
    PKG_DEPENDS_ON_DELIMS = r'[\s,]+'

    def __init__(self, ports_root_paths):
        # graph of node's dependencies
        # value of key is a list of nodes the key node depends on
        self.depends = defaultdict(list)
        # value of key is a list of packages that depend on key
        self.dependents = defaultdict(list)

        self.ports_root_paths = ports_root_paths

    def calc_deps(self):
        for x in self.ports_root_paths:
            for root, dirs, files in os.walk(x):
                for fname in files:
                    if fname == self.PKG_FILE_NAME:
                        self._process_pkgfile(join(root, fname))

    def _process_pkgfile(self, path):
        name = None
        deps = []
        with open(path) as f:
            for line in f:
                m = re.search(self.PKG_NAME_REGEX, line)
                if m:
                    name = m.group(1)
                m = re.search(self.PKG_DEPENDS_ON_REGEX, line)
                if m:
                    deps = re.split(self.PKG_DEPENDS_ON_DELIMS, m.group(1))
        self.depends[name] += deps
        for x in deps:
            self.dependents[x].append(name)

    def orphans(self):
        orps = []
        for x in self.depends:
            if not self.dependents[x]:
                orps.append(x)
        return orps

    def _deps(self, pkg):
        return self.depends[pkg]

    def _depts(self, pkg):
        return self.dependents[pkg]

    def deps(self, pkgs=None):
        if pkgs is None:
            return self.depends
        result = {}
        for pkg in pkgs:
            result[pkg] = self._deps(pkg)
        return result

    def depts(self, pkgs=None):
        if pkgs is None:
            return self.dependents
        result = {}
        for pkg in pkgs:
            result[pkg] = self._depts(pkg)
        return result

    def _rm(self, pkg):
        result = []
        if pkg not in self.depends:
            raise PrtdepException('cannot find "{}"'.format(pkg))
        dt = self.dependents[pkg]
        if dt:
            raise PrtdepException('cannot remove "{}", dependents: {}'.format(pkg, dt))
        else:
            queue = deque([pkg])
            while queue:
                foo = queue.popleft()
                result.append(foo)
                deps = self.depends[foo]
                depts = self.dependents[foo]
                del self.depends[foo]
                del self.dependents[foo]
                for x in deps:
                    self.dependents[x].remove(foo)
                for x in depts:
                    self.depends[x].remove(foo)

                for x in deps:
                    if not self.dependents[x]:
                        queue.append(x)

            return result

    def rm(self, pkgs):
        result = []
        for pkg in pkgs:
            result += self._rm(pkg)
        return result


def dump_dependencies(deps):
    print('dependencies:')
    print('=============')
    for x in deps:
        print('{}: {}'.format(x, deps[x]))
    print('')

def dump_dependents(depts):
    print('dependents:')
    print('===========')
    for x in depts:
        print('{}: {}'.format(x, depts[x]))
    print('')

def dump_all(prtdep):
    dump_dependencies(prtdep.deps())
    dump_dependents(prtdep.depts())

def process_info(args, prtdep):
    did_info = False
    if args['--dump']:
        dump_all(prtdep)
        did_info = True

    if args['--dump-deps']:
        dump_dependencies(prtdep.deps())
        did_info = True

    if args['--dump-dept']:
        dump_dependents(prtdep.depts())
        did_info = True

    if args['--orphans']:
        print('orphans:')
        print('========')
        print("\n".join(prtdep.orphans()))
        print('')
        did_info = True

    pkgs = args['--get-deps']
    if pkgs:
        print('dependencies:')
        print('=============')
        pkgs = pkgs.split(',')
        print(prtdep.deps(pkgs))
        print('')
        did_info = True
    pkgs = args['--get-dept']
    if pkgs:
        print('dependents:')
        print('===========')
        pkgs = pkgs.split(',')
        print(prtdep.depts(pkgs))
        print('')
        did_info = True
    return did_info


def main():
    import sys
    from docopt import docopt

    args = docopt(__doc__.format(sys.argv[0], __version__),
                  version=" ".join(('prtdep', __version__)))

    ports_roots = args['<ports-root-path>']
    prtdep = Prtdep(ports_roots)
    prtdep.calc_deps()

    info_after = args['--after']
    info_before = args['--before']
    info_before = info_before or (not info_after and not info_before)

    did_info = False
    if info_before:
        did_info = process_info(args, prtdep)

    pkgs = args['--remove']
    if pkgs:
        pkgs = pkgs.split(',')
        did_info = True
        try:
            result = prtdep.rm(pkgs)
            print('remove:')
            print('=======')
            print("\n".join(result))
            print('')
        except PrtdepException as pe:
            print(str(pe))

    if info_after:
        foo = process_info(args, prtdep)
        did_info = did_info or foo
    if not did_info:
        dump_all(prtdep)


if __name__ == '__main__':
    main()
