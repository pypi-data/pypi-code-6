#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jim_wan
#
# Created:     28/10/2014
# Copyright:   (c) jim_wan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'jimlib',
    version = '0.0.1',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'MIT License',

    author = 'jim',
    author_email = 'jim@126.com',

    packages = find_packages(),
    platforms = 'any',
)