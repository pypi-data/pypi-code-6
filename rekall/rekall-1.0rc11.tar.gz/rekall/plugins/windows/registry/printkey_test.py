# Rekall Memory Forensics
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Authors:
# Michael Cohen <scudette@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""Tests for the printkey plugin."""
import hashlib
import re
import os

from rekall import testlib


class TestPrintkey(testlib.RekallBaseUnitTestCase):
    """Test the printkey module."""

    PARAMETERS = dict(commandline="printkey")

    def testPrintkey(self):
        """Tests the printkey module."""
        previous = self.baseline['output']
        current = self.current['output']

        previous_blocks = sorted(
            self.SplitLines(previous, "----------"))

        current_blocks = sorted(
            self.SplitLines(current, "----------"))

        for x, y in zip(previous_blocks, current_blocks):
            self.assertEqual(x, y)


class TestRegDump(testlib.HashChecker):
    """Test dumping of registry hives."""

    PARAMETERS = dict(commandline="regdump --dump-dir %(tempdir)s")


class TestHiveDump(testlib.SimpleTestCase):
    PARAMETERS = dict(
        commandline="hivedump --hive_regex system32.config.default",
        )
