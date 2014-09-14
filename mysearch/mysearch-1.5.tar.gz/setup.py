#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
MySearch
Copyright (C) 2013   Tuxicoman

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import codecs
import os.path

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "mysearch", "version.txt"), "r") as f:
    VERSION = f.read().strip()

with codecs.open(os.path.join(HERE, 'README.txt'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="mysearch",
    version=VERSION,

    description='MySearch engine',
    long_description=LONG_DESCRIPTION,
    license="AGPL",

    url="http://codingteam.net/project/mysearch",
    author="Tuxicoman",
    author_email="debian@jesuislibre.net",

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
    ],
    keywords='web search privacy',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'Jinja2>=2.7',
        'Twisted>=13',
        'pyOpenSSL',
        'pyasn1>=0.1.7',
        'pyasn1-modules>=0.0.3',
    ],
    package_data={
        'mysearch': [
            'version.txt',
            'mysearch.tac',
            'static/*.ico', 'static/*.js', 'static/*.css', 'static/*.png', "templates/*.html", "templates/*.xml"
        ]
    },
)

