#!/usr/bin/env python

# setup.py
# Copyright (c) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from distutils.core import setup

long_description = """
This library reads and writes universal level formats.  These level
formats are generic enough to be used by any 2-D game.  Their purpose is
to unify level editing.
""".strip()

setup(name="ulvl",
      version="0.2.1",
      description="Simple universal level formats.",
      long_description=long_description,
      author="Julian Marchant",
      author_email="onpon4@riseup.net",
      url="https://www.gitorious.org/ulvl",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: Apache Software License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="Apache License 2.0",
      py_modules=["ulvl"],
      requires=[],
     )
