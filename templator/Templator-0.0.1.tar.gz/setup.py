#!/usr/bin/env python
# coding: utf-8

from __future__ import division, print_function, unicode_literals

import os
import sys

import templetor

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
required = open('r.txt').read().splitlines()


def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()
version = templetor.__version__
readme = open('README.rst').read()
setup(name='Templator',
      entry_points={'console_scripts': [
          'temp = templetor:main',
      ]},
      version=version,
      description='Distribution',
      # packages=[
      # 'templetor',
      #    ],
      package_dir={'templetor': 'templetor'},
      long_description=readme,
      author='Singularity',
      author_email='Singularitty@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      #      packages=['distutils', 'distutils.command'],
      packages=[b'templetor'],
      install_requires=required,
      #  license='GNU',
      license='ISC',
      classifiers=(
          #       'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          #        'Programming Language :: Python :: 3',
          #        'Programming Language :: Python :: 3.1',
          #        'Programming Language :: Python :: 3.2',
          #        'Topic :: Terminals :: Terminal Emulators/X Terminals',
      ),
      )
