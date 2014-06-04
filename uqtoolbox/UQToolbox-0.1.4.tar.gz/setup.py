#!/usr/bin/env python

#
# This file is part of UQToolbox.
#
# UQToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UQToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with UQToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

import os.path
import sys
from setuptools import setup, find_packages

deps = ['numpy',
        'scipy',
        'Sphinx',
        'prettytable',
        'SpectralToolbox >= 0.1']
if "--without-mpi4py" in sys.argv:
    idx = sys.argv.index('--without-mpi4py')
    del sys.argv[idx]
else:
    deps.append('mpi4py')

local_path = os.path.split(os.path.realpath(__file__))[0]
version_file = open(os.path.join(local_path, 'VERSION'))
version = version_file.read().strip()

setup(name = "UQToolbox",
      version = version,
      packages=find_packages(),
      include_package_data=True,
      scripts=[],
      url="http://www2.compute.dtu.dk/~dabi/index.php?slab=dtu-uq",
      author = "Daniele Bigoni",
      author_email = "dabi@dtu.dk",
      license="COPYING.LESSER",
      long_description=open("README.txt").read(),
      install_requires=deps
      )
