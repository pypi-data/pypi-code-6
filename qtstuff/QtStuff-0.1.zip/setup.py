#!/usr/bin/env python
from distutils.core import setup

""" Setup script for QtStuff """

setup(name = "QtStuff",
      version = "0.1",
      author = 'James Ramm',
      author_email = 'james.ramm@jbarisk.com',
      description = 'Useful classes for working with PySide\PyQt',
      url = 'https://github.com/JBARisk/QtStuff',
      packages = ['QtStuff'],
      package_data = {'QtStuff': ['Images/*.*', 'Images/GreyCircles/*.*', 'Images/OrangeIcons/*.*']})