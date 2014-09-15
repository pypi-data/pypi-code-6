#!/usr/bin/env python3

#
# trv: A graphical test result viewer
# Copyright (C) 2014 Canonical
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
#

import sys
assert sys.version_info >= (3,), 'Python 3 is required'

from setuptools import find_packages, setup
from trv import __version__


requires = [
    'PyQt5'
]


setup(
    name='trv',
    version=__version__,
    description='Graphical Test Result Viewer.',
    author='Thomi Richards',
    author_email='thomi.richards@canonical.com',
    url='https://launchpad.net/trv',
    license='GPLv3',
    packages=find_packages(),
    requires=requires,
    # test_suite='trv.tests',
    # tests_require=requires,
    entry_points={
        'console_scripts': ['trv = trv:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ]
)
