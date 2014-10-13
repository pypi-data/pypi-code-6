#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
from setuptools import setup
# from distutils.core import setup

setup(name='pymobile',
      version='0.1.0',
      description='Webframework using bottle, asyncio, websockets, jquery and jquery-mobile',
      long_description=open('README.txt').read(),
      author='Frode Holmer',
      author_email='fholmer@gmail.com',
      license='GPLv3',
      url='https://bitbucket.org/fholmer/pymobile',
      keywords='pymobile jquery mobile websocket asyncio bottle web framework',
      scripts=['pymobile-create-project'],
      package_dir = {'pymobile':'.'},
      packages=['pymobile', 'pymobile.controllers', 'pymobile.models'],
      package_data={'pymobile': ['views/*.*', 'static/*.*', 'static/*/*/*.*', 'static/*/*/*/*.*', 'static/*/*/*/*/*.*']},
      requires=['bottle', 'asyncio', 'websockets'],
      provides=['pymobile (0.1.0)'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: HTTP Servers'])
