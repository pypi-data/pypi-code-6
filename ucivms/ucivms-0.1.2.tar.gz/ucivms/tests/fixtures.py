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

from ucitests import fixtures
from ucivms import config


def isolate_from_disk(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup as well as an /etc/ one so tests can setup
    config files.
    """
    fixtures.set_uniq_cwd(test)
    fixtures.isolate_from_env(test)
    # Isolate tests from the user environment
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    os.environ['HOME'] = test.home_dir
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir, 'etc')
    os.mkdir(test.etc_dir)
    fixtures.patch(test, config, 'system_config_dir', lambda: test.etc_dir)
