#!/usr/bin/env python

from distutils.core import setup

setup(name='pyMeteor',
      version='0.0.4',
      description='Python tools for interacting with the Meteor web framework.',
      author='Matthew Goodman and Ted Blackman',
      author_email='software@3scan.com',
      url='https://github.com/3Scan/pyMeteor',
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
      ],
      requires=['ws4py(==0.3.2)'],
      py_modules=['pyMeteor'],
      )
