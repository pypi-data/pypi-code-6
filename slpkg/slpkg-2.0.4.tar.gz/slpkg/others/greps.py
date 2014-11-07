#!/usr/bin/python
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os

from slpkg.toolbar import status
from slpkg.__metadata__ import lib_path
from slpkg.splitting import split_package

from slpkg.slack.slack_version import slack_ver


def repo_data(PACKAGES_TXT, step, repo, version):
    '''
    Grap data packages
    '''
    (name, location, size, unsize,
     rname, rlocation, rsize, runsize) = ([] for i in range(8))
    index, toolbar_width = 0, 700
    for line in PACKAGES_TXT.splitlines():
        index += 1
        toolbar_width = status(index, toolbar_width, step)
        if line.startswith("PACKAGE NAME"):
            name.append(line[15:].strip())
        if line.startswith("PACKAGE LOCATION"):
            location.append(line[21:].strip())
        if line.startswith("PACKAGE SIZE (compressed):  "):
            size.append(line[28:-2].strip())
        if line.startswith("PACKAGE SIZE (uncompressed):  "):
            unsize.append(line[30:-2].strip())
    if repo == "rlw":
        (rname,
         rlocation,
         rsize,
         runsize
         ) = rlw_filter(name, location, size, unsize)
    elif repo == "alien":
        (rname,
         rlocation,
         rsize,
         runsize
         ) = alien_filter(name, location, size, unsize, version)
    elif repo == "slacky":
        rname, rlocation, rsize, runsize = name, location, size, unsize
    return [rname, rlocation, rsize, runsize]


def rlw_filter(name, location, size, unsize):
    '''
    Filter rlw repository data
    '''
    arch = os.uname()[4]
    if arch.startswith("i") and arch.endswith("86"):
        arch = "i486"
    (fname, flocation, fsize, funsize) = ([] for i in range(4))
    for n, l, s, u in zip(name, location, size, unsize):
        loc = l.split("/")
        if arch == loc[-1]:
            fname.append(n)
            flocation.append(l)
            fsize.append(s)
            funsize.append(u)
    return [fname, flocation, fsize, funsize]


def alien_filter(name, location, size, unsize, version):
    '''
    Filter alien repository data
    '''
    ver = slack_ver()
    if version == "current":
        ver = "current"
    path_pkg = "pkg"
    if os.uname()[4] == "x86_64":
        path_pkg = "pkg64"
    (fname, flocation, fsize, funsize) = ([] for i in range(4))
    for n, l, s, u in zip(name, location, size, unsize):
        if path_pkg == l.split("/")[-2] and ver == l.split("/")[-1]:
            fname.append(n)
            flocation.append(l)
            fsize.append(s)
            funsize.append(u)
    return [fname, flocation, fsize, funsize]


def repo_requires(name, repo):
    '''
    Grap package requirements from alien repository
    '''
    lib = {
        'alien': lib_path + "alien_repo/PACKAGES.TXT",
        'slacky': lib_path + "slacky_repo/PACKAGES.TXT"
    }
    f = open(lib[repo], "r")
    PACKAGES_TXT = f.read()
    f.close()
    for line in PACKAGES_TXT.splitlines():
        if line.startswith("PACKAGE NAME: "):
            pkg = line[14:].strip()
            pkg_name = split_package(pkg)[0]
        if line.startswith("PACKAGE REQUIRED: "):
            if pkg_name == name:
                return line[18:].strip().split(",")
