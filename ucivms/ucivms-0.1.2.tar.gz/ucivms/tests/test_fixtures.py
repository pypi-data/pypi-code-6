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

import os
import unittest

from ucitests import assertions

from ucivms.tests import fixtures


class TestIsolateFromDisk(unittest.TestCase):

    def test_disk_preserved(self):
        real_home = os.path.expandvars('$HOME')

        class Inner(unittest.TestCase):

            def test_overridden(self):
                fixtures.isolate_from_disk(self)
                # We know expanduser will use $HOME which is set by
                # isolate_from_disk
                self.assertNotEqual(real_home, os.path.expandvars('$HOME'))
                path = os.path.expanduser('~/testing')
                with open(path, 'w') as f:
                    f.write('whatever')
                # Make sure the file is created in the right place
                self.assertTrue(os.path.exists(path))

        assertions.assertSuccessfullTest(self, Inner('test_overridden'))
        # Make sure the file wasn't created in the wrong place
        self.assertFalse(os.path.exists('~/testing'))
