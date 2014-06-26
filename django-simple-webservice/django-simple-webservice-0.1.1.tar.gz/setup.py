#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-simple-webservice
# Copyright (c) 2014, Liricus, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.


#==============================================================================
# DOCS
#==============================================================================

"""This file is for distribute

"""


#==============================================================================
# IMPORTS
#==============================================================================

import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

#==============================================================================
# CONSTANTS
#==============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS = [
    "Django>=1.6.5"
]


#==============================================================================
# META
#==============================================================================

# : This is the project name
PRJ = "django-simple-webservice"

# : The project version as tuple of strings
VERSION = ("0", "1", "1")

# : The project version as string
STR_VERSION = ".".join(VERSION)
__version__ = STR_VERSION

# : For "what" is usefull simple-ws
DOC = """Django app for simple create  json-rpc like webservices"""

# : The short description for pypi
SHORT_DESCRIPTION = []
for line in DOC.splitlines():
    if not line.strip():
        break
    SHORT_DESCRIPTION.append(line)
SHORT_DESCRIPTION = u" ".join(SHORT_DESCRIPTION)
del line

# : Clasifiers for optimize search in pypi
CLASSIFIERS = (
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
)

# : Home Page of simple-ws
URL = "https://bitbucket.org/liricus/django-simple-webservice"

# : Author of this simple-ws
AUTHOR = "Liricus SRL"

# : Email ot the autor
EMAIL = "info@liricus.com.ar"

# : The license name
LICENSE = "LGPL"

# : The license of simple-ws
FULL_LICENSE = u"""" django-simple-webservice
Copyright (c) 2014, Liricus, All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.

"""

# : Keywords for search of pypi
KEYWORDS = """webservices json simple django"""


#==============================================================================
# FUNCTIONS
#==============================================================================

setup(
    name=PRJ.lower(),
    version=STR_VERSION,
    description=SHORT_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=[pkg for pkg in find_packages() if pkg.startswith("simple_webservice")],
    include_package_data=True,
    py_modules=["ez_setup"],
    install_requires=REQUIREMENTS,
)
