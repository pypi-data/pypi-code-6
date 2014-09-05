#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup
import os

from b2tool import __projectname__

ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
  name=__projectname__,
  version='0.0.4',
  url="https://github.com/jesuejunior/b2tool",
  license="3-BSD",
  description='bbtool is a command line tool to manage BitBucket',
  author="Jesue Junior",
  author_email="talkto@jesuejunior.com",
  long_description=open(os.path.join(ROOT, 'README.rst')).read(),
  packages=['b2tool', 'b2tool/commands'],
    entry_points={
        'console_scripts': [
            'b2tool = b2tool.main:main',
            ]
    },
  install_requires = ['komandr==0.1.1', 'requests==2.3.0', 'clint==0.3.7'],
  classifiers = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Application Frameworks"
    ])