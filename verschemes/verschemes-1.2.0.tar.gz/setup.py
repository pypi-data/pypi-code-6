#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup.py for the verschemes project"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future import utils

import os

from setuptools import setup


THIS_DIRECTORY = os.path.dirname(__file__)

def read_file(path):
    return open(os.path.join(THIS_DIRECTORY, path)).read()

# Set __version_info__ and __version__ from the _version.py module code.
exec(read_file(os.path.join('src', 'verschemes', '_version.py')))

setup(
    name='verschemes',
    version=__version__,
    author="Craig Hurd-Rindy",
    author_email="gnuworldman@gmail.com",
    maintainer="Craig Hurd-Rindy",
    maintainer_email="gnuworldman@gmail.com",
    url='https://github.com/gnuworldman/verschemes',
    description="Version identifier management",
    long_description=read_file('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        ],
    package_dir={'': 'src'},
    packages=[utils.native_str('verschemes'),
              utils.native_str('verschemes.future')],
    install_requires=['future'],
    )
