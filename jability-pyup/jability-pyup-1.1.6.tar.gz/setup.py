#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from distutils.core import setup

setup(
    name = 'jability-pyup',
    version = '1.1.6',
    description = 'Jability Python Utilities Package',
    author = 'Fabrice Romand',
    author_email = 'fabrice.romand@gmail.com',
    maintainer = 'Fabrice Romand',
    maintainer_email = 'fabrice.romand@gmail.com',
    #url = 'http://jability.org/pyup/',
    #download_url = 'http://jability.org/pyup/download/',
    packages = [    'jabilitypyup',
                    'jabilitypyup.amqp',
                    'jabilitypyup.hl7'],
    license = 'GPL v2'
    )
