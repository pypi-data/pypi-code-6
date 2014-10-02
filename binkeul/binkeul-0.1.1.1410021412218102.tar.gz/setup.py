#!/usr/bin/env python3
#coding:utf-8
# Author:  budl
# Purpose: setup
# Created: 2014.9.30
# License: LGPL

import os
from setuptools import setup

VERSION = '0.1.1'
AUTHOR_NAME = 'Budl Doiksea'
AUTHOR_EMAIL = 'ikw3179@naver.com'


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname


setup(name='binkeul',
      version=VERSION,
      description='A Python library to support Binkeul (construct language)',
      author=AUTHOR_NAME,
      url='http://bitbucket.org/sinabilo/binkeul',
      download_url='http://bitbucket.org/sinabilo/binkeul/downloads',
      author_email=AUTHOR_EMAIL,
      packages=['binkeul'],
      provides=['binkeul'],
      package_dir={'binkeul': 'binkeul'},
      package_data={'binkeul': ['_static/*.json',"_static/ppdb.sqlite",'test/test-*','test/__head.py','test/_img/*']},
      install_requires=['pillow>=2.3.0'],
      long_description=read('README.TXT') + read('NEWS.TXT'),
      platforms="OS Independent",
      license="LGPL",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Intended Audience :: Developers",
          "Topic :: Multimedia :: Graphics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ]
)
