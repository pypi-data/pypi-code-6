#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='grepurl',
      version='0.1.1',
      description='extract URLs from websites on the command line',
      long_description=README,
      author='Gerome Fournier',
      maintainer='Arne Neumann',
      maintainer_email='grepurl.programming@arne.cl',
      url='https://github.com/arne-cl/grepurl',
      py_modules=['grepurl'],
      entry_points={'console_scripts': ['grepurl=grepurl:main']},
      license='GPLv2 or later',
)


