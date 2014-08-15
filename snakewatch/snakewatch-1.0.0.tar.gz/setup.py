"""
This file is part of snakewatch.

snakewatch is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

snakewatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with snakewatch.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import os

from setuptools import setup, find_packages

from snakewatch import NAME, VERSION, DESCRIPTION, URL, AUTHOR, AUTHOR_EMAIL

extra_options = dict(
)
options = dict(
)


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()


setup(
    name=NAME,
    version=VERSION,
    
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    
    url=URL,
    description=DESCRIPTION,
    keywords='log, tail',
    long_description=read('README'),

    packages=find_packages(),
    install_requires=['colorama', 'six'],
    
    entry_points={
        'console_scripts': [
            'snakewatch = snakewatch.main:main',
        ],
    },

    license='LGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Logging',
    ],

    options=options,
    **extra_options
)
