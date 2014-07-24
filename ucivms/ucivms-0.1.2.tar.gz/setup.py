#!/usr/bin/env python

# This file is part of the Ubuntu Continuous Integration virtual machine tools
#
# Copyright 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


from  distutils import core

import ucivms


core.setup(
    name='ucivms',
    version='.'.join(str(c) for c in ucivms.__version__[0:3]),
    description=('Ubuntu Continuous Integration virtual machine tools.'),
    author='Vincent Ladeuil',
    author_email='vila+ci@canonical.com',
    url='https://launchpad.net/uci-vms',
    license='GPLv3',
    install_requires=['uciconfig'],
    packages=['ucivms', 'ucivms.tests'],
    scripts=['uci-vms'],
)
