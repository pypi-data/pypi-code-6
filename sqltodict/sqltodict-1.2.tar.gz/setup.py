#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sqltodict import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

setup(
  name = 'sqltodict',
  packages = ['sqltodict'],
  version = __version__,
  description = 'Raw sql results returns as dictionary.',
  author = u'Barbaros YILDIRIM',
  author_email = 'barbarosaliyildirim@gmail.com',
  url = 'https://github.com/RedXBeard/python-sqldict',
  download_url = 'https://github.com/RedXBeard/python-sqldict/tarball/%s'%__version__,
  keywords = ['sql','dict','sql to dict','select results as dict',
              'sql to dictionary', 'postgresql select as dictionary',
              'postgress results as dict'],
  classifiers = [
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Environment :: Console',
    'Programming Language :: Python :: 2.7',
    'Natural Language :: English',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
  ],
  long_description = long_description,
  install_requires=['psycopg2>=2.5.4','mysql-connector-repackaged>=0.3.1']
)
