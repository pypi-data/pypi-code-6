#!/usr/bin/env python

# Copyright 2014 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from setuptools import setup

VERSIONFILE = "sqlalchemy_find.py"


def get_version():
    return re.search("^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                     read(VERSIONFILE), re.M).group(1)


def read(*path):
    """\
    Read and return contents of ``path``
    """
    with open(os.path.join(os.path.dirname(__file__), *path),
              'rb') as f:
        return f.read().decode('UTF-8')

setup(
    name='sqlalchemy-find',
    version=get_version(),
    url='https://bitbucket.org/ollyc/sqlalchemy-find',

    license='BSD',
    author='Oliver Cope',
    author_email='oliver@redgecko.org',

    description='Syntactic sugar for SQLAlchemy: a Storm ORM-like find method',
    long_description=read('README.rst') + "\n\n" + read("CHANGELOG.rst"),
    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python'],

    py_modules=['sqlalchemy_find'],
    packages=[],

    install_requires=['sqlalchemy'],
    setup_requires=[],
    tests_require=[],
)
