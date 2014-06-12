# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the Juju Quickstart platform management."""

from __future__ import unicode_literals

import mock
import unittest

from quickstart import (
    platform_support,
    settings,
)


class TestGetPlatform(unittest.TestCase):

    def patch_platform_system(self, system=None):
        """Patch the platform.system call to return the given value."""
        mock_patch_platform = mock.Mock(return_value=system)
        path = 'quickstart.platform_support.platform.system'
        return mock.patch(path, mock_patch_platform)

    def patch_isfile(self, values):
        mock_patch_isfile = mock.Mock(side_effect=iter(values))
        path = 'quickstart.platform_support.os.path.isfile'
        return mock.patch(path, mock_patch_isfile)

    def test_linux_apt(self):
        with self.patch_platform_system('Linux'):
            with self.patch_isfile([True]):
                result = platform_support.get_platform()
        self.assertEqual(settings.LINUX_APT, result)

    def test_linux_rpm(self):
        with self.patch_platform_system('Linux'):
            with self.patch_isfile([False, True]):
                result = platform_support.get_platform()
        self.assertEqual(settings.LINUX_RPM, result)

    def test_osx(self):
        with self.patch_platform_system('Darwin'):
            result = platform_support.get_platform()
        self.assertEqual(settings.OSX, result)

    def test_windows(self):
        with self.patch_platform_system('Windows'):
            result = platform_support.get_platform()
        self.assertEqual(settings.WINDOWS, result)

    def test_unsupported_raises_exception(self):
        with self.patch_platform_system('CP/M'):
            with self.assertRaises(platform_support.UnsupportedOS) as exc:
                platform_support.get_platform()
        self.assertEqual('CP/M', exc.exception.message)

    def test_linux_no_apt_nor_rpm_raises_exception(self):
        with self.patch_platform_system('Linux'):
            with self.patch_isfile([False, False]):
                with self.assertRaises(
                        platform_support.UnsupportedOS) as context:
                    platform_support.get_platform()
        self.assertEqual(
            'Linux without apt-get nor rpm', context.exception.message)

    def test_null_system(self):
        # If platform.system cannot determine the OS it returns ''.  We have a
        # special case to return a meaningful message in that situation.
        with self.patch_platform_system(''):
            with self.assertRaises(platform_support.UnsupportedOS) as context:
                platform_support.get_platform()
        self.assertEqual(
            'Unable to determine the OS platform', context.exception.message)


class TestSupportLocal(unittest.TestCase):

    def test_support_local(self):
        expected = {
            settings.LINUX_APT: True,
            settings.LINUX_RPM: True,
            settings.OSX: False,
            settings.WINDOWS: False,
            object(): False,
        }
        for key, value in expected.items():
            self.assertEqual(value, platform_support.supports_local(key))


class TestGetJujuInstaller(unittest.TestCase):

    def test_linux_apt(self):
        platform = settings.LINUX_APT
        installer = platform_support.get_juju_installer(platform)
        self.assertEqual(platform_support._installer_apt, installer)

    def test_osx(self):
        platform = settings.OSX
        installer = platform_support.get_juju_installer(platform)
        self.assertEqual(platform_support._installer_osx, installer)

    def test_linux_rpm(self):
        platform = settings.LINUX_RPM
        with self.assertRaises(platform_support.UnsupportedOS) as ctx:
            platform_support.get_juju_installer(platform)
        self.assertEqual(
            'No installer found for host platform.', ctx.exception.message)

    def test_windows(self):
        platform = settings.WINDOWS
        with self.assertRaises(platform_support.UnsupportedOS) as ctx:
            platform_support.get_juju_installer(platform)
        self.assertEqual(
            'No installer found for host platform.', ctx.exception.message)
