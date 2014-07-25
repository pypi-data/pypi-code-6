# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
rhodecode.lib.paster_commands.make_config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

depracated make-config paster command for RhodeCode

:created_on: Oct 10, 2013
:author: marcink
:copyright: (c) 2013 RhodeCode GmbH.
:license: GPLv3, see LICENSE for more details.
"""

import os
import sys
from paste.script.appinstall import AbstractInstallCommand
from paste.script.command import BadCommand
from paste.deploy import appconfig

# fix rhodecode import
from os.path import dirname as dn
rc_path = dn(dn(dn(os.path.realpath(__file__))))
sys.path.append(rc_path)

class Command(AbstractInstallCommand):

    default_verbosity = 1
    max_args = None
    min_args = 1
    summary = "*DEPRECATED* Install a package and create a fresh config file/directory"
    usage = "PACKAGE_NAME [CONFIG_FILE] [VAR=VALUE]"

    description = """\
    Note: this is an experimental command, and it will probably change
    in several ways by the next release.

    make-config is part of a two-phase installation process (the
    second phase is setup-app).  make-config installs the package
    (using easy_install) and asks it to create a bare configuration
    file or directory (possibly filling in defaults from the extra
    variables you give).
    """

    parser = AbstractInstallCommand.standard_parser(
        simulate=True, quiet=True, no_interactive=True)

    def command(self):
        sys.stderr.write(
            '** Warning **\n'
            'This command is now removed and depracated, please '
            'use new rhodecode-config command instead.')
        sys.exit(-1)
    def update_parser(self):
        pass
