#!/usr/bin/env python
# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import sys

install_requires = []
if sys.version_info < (2, 7):
    install_requires.append('argparse')

setuptools.setup(
    name='argparse-safe',
    version='1.0.0',
    description='Safely transitively depend on argparse',
    long_description=open("README.rst").read(),
    url='http://github.com/emonty/argparse-safe',
    license='Apache',
    author='Monty Taylor',
    author_email='mordred@inaugust.com',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
    ],
)
