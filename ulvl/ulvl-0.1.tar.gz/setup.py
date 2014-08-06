#!/usr/bin/env python

# setup.py
# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
from distutils.core import setup

long_description = """
This library reads and writes universal level formats.  These level
formats are generic enough to be used by any 2-D game.  Their purpose is
to unify level editing.
""".strip()

setup(name="ulvl",
      version="0.1",
      description="Simple universal JSON level format.",
      long_description=long_description,
      author="Julian Marchant",
      author_email="onpon4@riseup.net",
      url=None,
      classifiers=["Development Status :: 3 - Alpha",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="Expat License",
      py_modules=["ulvl"],
      requires=[],
     )
