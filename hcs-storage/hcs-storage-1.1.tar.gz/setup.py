#!/usr/bin/env python
# vim: fileencoding=UTF-8 filetype=python ff=unix expandtab sw=4 sts=4 tw=120
# author: Christer Sjöholm -- goobook AT furuvik DOT net

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '1.1'

setup(name='hcs-storage',
      version=version,
      description="My personal library collecting some useful snippets.",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='',
      author='Christer Sjöholm',
      author_email='hcs at furuvik dot net',
      url='http://pypi.python.org/pypi/hcs-storage',
      download_url='http://pypi.python.org/pypi/hcs-storage',
      py_modules=['storage'],
      zip_safe=True,
      install_requires=[
          'six'
          ],
      entry_points={
          # -*- Entry points: -*-
          }
      )
