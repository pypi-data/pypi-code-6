# -*- coding: utf-8 -*-
"""
################################################################################
# Copyright (c) 2010, Ilgar Mashayev
# Copyright (c) 2014, VNC AG
# 
# E-mail: support@vnc.biz
# Website: http://github.com/vnc-biz/pyzimbra
################################################################################
# This file is part of pyzimbra.
# 
# Pyzimbra is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Pyzimbra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Pyzimbra.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

Distutil setup.

@author: ilgar
"""

from setuptools import setup, find_packages

files = ["*", "z/*"]

setup(name = 'pyzimbra',
    version = '0.1',
    license = 'LGPL',
    description = 'Zimbra Python Client',
    long_description=open("README.rst").read(),
    author = 'Ilgar Mashayev',
    author_email = 'pyzimbra@lab.az',
    url = 'http://github.com/ilgarm/pyzimbra',
    packages = ['pyzimbra','pyzimbra/z', 'pyzimbra/z/zobject/'],
    package_data = {'package' : files },
    install_requires=[
        'SOAPpy',
    ],
)
