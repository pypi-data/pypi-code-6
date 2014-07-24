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
from __future__ import unicode_literals


from cStringIO import StringIO
import unittest


from ucitests import fixtures
from ucivms import (
    errors,
    monitors,
)
from ucivms.tests import (
    fixtures as vms_fixtures,
)


class TestConsoleParsing(unittest.TestCase):

    def _scan_console_monitor(self, string):
        mon = monitors.ConsoleMonitor(StringIO(string))
        lines = []
        for line in mon.scan():
            lines.append(line)
        return lines

    def test_fails_on_empty(self):
        with self.assertRaises(errors.ConsoleEOFError):
            self._scan_console_monitor('')

    def test_fail_on_knwon_cloud_init_errors(self):
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor('Failed loading yaml blob\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                'Unhandled non-multipart userdata starting\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                "failed to render string to stdout: cannot find 'uptime'\n")
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                "Failed loading of cloud config "
                "'/var/lib/cloud/instance/cloud-config.txt'. "
                "Continuing with empty config\n")

    def test_succeds_on_final_message(self):
        lines = self._scan_console_monitor('''
Lalala
I'm doing my work
It goes nicely
uci-vms finished installing in 1 seconds.
That was fast isn't it ?
 * Will now halt
[   33.204755] Power down.
''')
        # We stop as soon as we get the final message and ignore the rest
        self.assertEquals(' * Will now halt\n',
                          lines[-1])


class TestConsoleParsingWithFile(unittest.TestCase):

    def setUp(self):
        super(TestConsoleParsingWithFile, self).setUp()
        vms_fixtures.isolate_from_disk(self)

    def _scan_file_monitor(self, string):
        with open('console', 'w') as f:
            f.write(string)
        mon = monitors.TailMonitor('console')
        for line in mon.scan():
            pass
        return mon.lines

    def test_succeeds_with_file(self):
        content = '''\
Yet another install
Going well
uci-vms finished installing in 0.5 seconds.
Wow, even faster !
 * Will now halt
Whatever, won't read that
'''
        lines = self._scan_file_monitor(content)
        expected_lines = content.splitlines(True)
        # Remove the last line that should not be seen
        expected_lines = expected_lines[:-1]
        self.assertEqual(expected_lines, lines)

    def xtest_fails_on_empty_file(self):
        # FIXME: We need some sort of timeout there... -- vila 2013-ish
        with self.assertRaises(errors.CommandError):
            self._scan_file_monitor('')

    def test_fail_on_knwon_cloud_init_errors_with_file(self):
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor('Failed loading yaml blob\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor(
                'Unhandled non-multipart userdata starting\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor(
                "failed to render string to stdout: cannot find 'uptime'\n")


class TestActualFileSize(unittest.TestCase):

    def setUp(self):
        super(TestActualFileSize, self).setUp()
        fixtures.set_uniq_cwd(self)

    def assertSize(self, expected, path):
        self.assertEqual(expected, monitors.actual_file_size(path))

    def test_empty_file(self):
        open('foo', 'w').close()
        self.assertSize(0, 'foo')

    def test_file_with_content(self):
        with open('foo', 'w') as f:
            f.write('bar')
        self.assertSize(3, 'foo')

    def test_unknown_file(self):
        self.assertSize(None, 'I-dont-exist')
