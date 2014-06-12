#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# éClaircie
# Copyright (C) 2014 Jean-Baptiste LAMY

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, os.path, sys, glob

HERE = os.path.dirname(sys.argv[0]) or "."

if len(sys.argv) <= 1: sys.argv.append("install")


import distutils.core, distutils.sysconfig
if ("upload_docs" in sys.argv) or ("build_sphinx" in sys.argv): import setuptools

install_dir = distutils.sysconfig.get_python_lib()

distutils.core.setup(
  name         = "eClaircie",
  version      = "0.1",
  license      = "GPLv3+",
  description  = "éClaircie is a 100% static and cloud-less blog engine. It is based on the Sphinx documentation generator.",
  long_description = open(os.path.join(HERE, "README.rst")).read(),
  
  author       = "Lamy Jean-Baptiste (Jiba)",
  author_email = "<jibalamy *@* free *.* fr>",
  url          = "https://bitbucket.org/jibalamy/eclaircie",
  classifiers  = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: POSIX :: Linux",
    "Environment :: Web Environment",
    "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
  
  requires = ["pillow", "sphinx"],
  
  scripts      = ["eclaircie"],
  package_dir  = {"eclaircie" : "."},
  packages     = ["eclaircie"],
  #package_data = {"eclaircie" : ["themes/*"]}
  #package_data = {"eclaircie" : ["themes/%s" for file in os.listdir(os.path.join(HERE, "themes"))]}
  package_data = {"eclaircie" : ["themes/*", "themes/*/*", "themes/*/*/*"]}
  #package_data = {"pymedtermino" : ["%s" % file for file in os.listdir(HERE) if file.endswith(".sqlite3")]}
  )
