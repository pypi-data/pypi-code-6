#!/usr/bin/python
# -*- coding: utf-8 -*-

# setup.py file is part of alarm.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/alarm

# Alarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from alarm import __version__, __email__

setup(
    name="alarm",
    packages=["alarm"],
    scripts=["bin/alarm"],
    version=__version__,
    description="CLI Alarm Clock",
    keywords=["alarm", "clock", "CLI"],
    author="dslackw",
    author_email=__email__,
    url="https://github.com/dslackw/alarm",
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "Development Status :: 3 - Alpha"],
    long_description=open("README.rst").read()
)
