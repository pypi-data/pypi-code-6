#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------
# Copyright (c) 2014 Eren Inan Canpolat
# Author: Eren Inan Canpolat <eren.canpolat@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------

from setuptools import setup
import re

version = "0.1.9"
description = "ePub generation from Google Documents"
url = "https://github.com/canpolat/bookbinder"
author = "Eren Inan Canpolat"
author_email = "eren.canpolat@gmail.com"

setup(name='bookbinder',
	version=version,
	description=description,
	long_description=open('README.rst').read(),
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Natural Language :: English',
		'Programming Language :: Python :: 2.7',
	],
	url=url,
	author=author,
	author_email=author_email,
	packages=['bookbinder'],
	entry_points={
		'console_scripts': [
			'bookbinder = bookbinder:bindbook',
		],
	},
	install_requires=[
		"Genshi>=0.6",
		"Markdown>=2.4",
		"beautifulsoup4>=4.3.2",
		"cssutils>=1.0",
		"google-api-python-client>=1.2",
	],
	include_package_data=True,
	zip_safe=False)
