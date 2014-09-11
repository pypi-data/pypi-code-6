#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lime
# @Date:   2014-09-11 17:11:56
# @Last Modified by:   Lime
# @Last Modified time: 2014-09-11 19:45:27

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
except:
    README = '''`reverseip` is a tool which can find possible domain names with the given ip(s).'''

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: No Input/Output (Daemon)',
    'Intended Audience :: System Administrators',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: System :: Boot',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Systems Administration',
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
]

dist = setup(
    name='reverseip',
    version='1.0.1',
    license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
    url='https://github.com/shiyanhui/reverseip',
    description="`reverseip` is a tool which can find possible domain names with the given ip(s).",
    long_description=README,
    classifiers=CLASSIFIERS,
    author="Lime YanhuiShi",
    author_email="lime.syh@gmail.com",
    maintainer="Lime YanhuiShi",
    maintainer_email="lime.syh@gmail.com",
    packages=find_packages(),
    install_requires=[
        'gevent >= 1.0.1',
        'beautifulsoup4 >= 4.3.2'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'reverseip = reverseip.__init__:main'
        ],
    },
)