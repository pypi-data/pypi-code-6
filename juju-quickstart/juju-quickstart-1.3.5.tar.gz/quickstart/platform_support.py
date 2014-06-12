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

"""Juju Quickstart platform management."""

from __future__ import (
    print_function,
    unicode_literals,
)

import os
import platform
from quickstart import utils
from quickstart import settings


class UnsupportedOS(Exception):
    """Raised if an unsupported OS is detected.

    This situation includes a linux system that has neither apt-get nor rpm
    installed.
    """
    pass


def get_platform():
    """Return the platform of the host.

    Raises UnsupportedOS if a platform we don't support is detected.
    """
    system = platform.system()
    if system == 'Darwin':
        return settings.OSX
    elif system == 'Windows':
        return settings.WINDOWS
    elif system == 'Linux':
        if os.path.isfile('/usr/bin/apt-get'):
            return settings.LINUX_APT
        elif os.path.isfile('/usr/bin/rpm'):
            return settings.LINUX_RPM
        raise UnsupportedOS(b'{} without apt-get nor rpm'.format(system))
    elif system == '':
        raise UnsupportedOS(b'Unable to determine the OS platform')
    raise UnsupportedOS(system)


def _installer_apt(distro_only, required_packages):
    """Perform package installation on Linux with apt.

    Raises OSError if the called functions raise it or an error is
    encountered.
    """
    if not distro_only:
        utils.add_apt_repository('ppa:juju/stable')
    print('sudo privileges will be used for the installation of \n'
          'the following packages: {}\n'
          'this can take a while...'.format(', '.join(required_packages)))
    retcode, _, error = utils.call(
        'sudo', '/usr/bin/apt-get', 'install', '-y', *required_packages)
    if retcode:
        raise OSError(bytes(error))


def _installer_osx(distro_only, required_packages):
    """Perform package installation on OS X via brew.

    Note distro_only is meaningless on OS X as there is no PPA option.  It is
    silently ignored.
    Raises OSError if the called functions raise it or an error is
    encountered.
    """
    print('Installing the following packages: {}\n'.format(
        ', '.join(required_packages)))
    retcode, _, error = utils.call(
        '/usr/local/bin/brew', 'install', *required_packages)
    if retcode:
        raise OSError(bytes(error))


INSTALLERS = {
    settings.LINUX_APT: _installer_apt,
    settings.OSX: _installer_osx,
}


def get_juju_command(platform):
    """Return the path to the Juju command on the given platform.

    If the platform does not have a novel location, the default will be
    returned.
    """
    return settings.JUJU_CMD_PATHS.get(
        platform,
        settings.JUJU_CMD_PATHS['default'])


def get_juju_installer(platform):
    """Return the installer for the host platform.

    Returns installer callable.
    Raises UnsupportedOS if a platform we don't support is detected.
    """
    installer = INSTALLERS.get(platform)
    if installer is None:
        raise UnsupportedOS(b'No installer found for host platform.')
    return installer


def supports_local(platform):
    """Return True if the platform supports local (LXC) deploys."""
    return platform in (settings.LINUX_APT, settings.LINUX_RPM)
