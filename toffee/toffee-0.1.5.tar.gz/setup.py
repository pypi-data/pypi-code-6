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

VERSIONFILE = "toffee.py"


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
    name='toffee',
    version=get_version(),
    url='https://bitbucket.org/ollyc/toffee',

    license='BSD',
    author='Oliver Cope',
    author_email='oliver@redgecko.org',

    description='Toffee: Test Object Fixture Factories - '
                'easy creation of data fixtures for tests',
    long_description=read('README.rst') + "\n\n" + read("CHANGELOG.rst"),
    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Topic :: Software Development :: Testing',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3'],

    keywords='fixtures fixture data test testing sqlalchemy storm django',

    py_modules=['toffee'],
    packages=[],

    install_requires=[],
    setup_requires=[],
    tests_require=[],
)
