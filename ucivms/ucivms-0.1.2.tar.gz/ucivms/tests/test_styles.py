# This file is part of Ubuntu Continuous Integration virtual machine tools.
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

from ucitests.tests import test_styles

import ucivms


class TestPep8(test_styles.TestPep8):

    packages = [ucivms]


class TestPyflakes(test_styles.TestPyflakes):

    packages = [ucivms]
