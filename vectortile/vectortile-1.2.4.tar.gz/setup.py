#!/usr/bin/env python

from glob import glob
from os.path import sep
from distutils.core import setup

import vectortile

setup(name='vectortile',
      version=vectortile.__version__,
      author=vectortile.__author__,
      author_email='paul@skytruth.org',
      description=vectortile.__doc__,
      long_description=vectortile.__doc__,
      url=vectortile.__source__,
      license=vectortile.__license__,
      packages=['vectortile', 'vectortile.tests'],
      install_requires=['python-geohash']
)
