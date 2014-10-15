#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
#
# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.core import setup
from setuptools import setup, find_packages
from distutils.command.build import build as _build

import iflux
import iflux.conf
from iflux.util import file
import os, sys
import subprocess


HG_LATEST_TAG_LABEL_CMD = 'hg log -r tip --template "{latesttag}.{latesttagdistance}"'
IFLUX_BUILD_FILE = os.path.join(os.path.dirname(__file__), 'build/lib/iflux/__init__.py')

def get_iflux_version():
    proc = subprocess.Popen(HG_LATEST_TAG_LABEL_CMD, shell=True,stdout=subprocess.PIPE)
    stdout_list = proc.communicate()[0].split('.')
    return stdout_list[-1]

def get_versioned_iflux_file_content():
    iflux_file_content = file.read(IFLUX_BUILD_FILE)
    return iflux_file_content.replace('"_REVISION_"', get_iflux_version())

class CustomBuildCommand(_build):
    def run(self):
        _build.run(self)
        dist_file = os.path.join(os.getcwd(), 'PKG-INFO')
        if not os.path.exists(dist_file):
            #TODO Add the static script routine here
            file.write(IFLUX_BUILD_FILE, get_versioned_iflux_file_content())

install_requires = [
        "tornado>=3.2",
        "redis>=2.9.1",
        "sqlalchemy==0.9.4",
    ] 

setup(
    name='iFlux',
    version= iflux.__version__.replace('_REVISION_', get_iflux_version()),
    description='iFlux is a python web framework based on Tornado web framework/server.',
    license='Apache License V2.0',
    author='Flavio Garcia',
    author_email='piraz@candango.org',
    install_requires=install_requires,
    cmdclass={
        'build': CustomBuildCommand,
    },
    url='http://www.candango.org/p/iflux',
    packages=[
        'iflux',
        'iflux.core', 
        'iflux.core.data',
        'iflux.core.scaffolding', 
        'iflux.core.session',
        'iflux.modules',
        'iflux.modules.admin',
        'iflux.modules.iflux',
        'iflux.util',
    ],
    package_dir={'iflux': 'iflux'},
    package_data={'iflux': ['conf/*.ini', 'modules/*/templates/*.html']},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    scripts=['iflux/bin/iflux-admin.py'],
    entry_points={'console_scripts': [
        'iflux = iflux.core.scaffolding:run_from_command_line',
    ]},
)

