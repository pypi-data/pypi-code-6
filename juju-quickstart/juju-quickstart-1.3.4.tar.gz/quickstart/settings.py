# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2013-2014 Canonical Ltd.
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

"""Juju Quickstart settings."""

from __future__ import unicode_literals

import collections
import os

# Platforms.
OSX = object()
LINUX_APT = object()
LINUX_RPM = object()
WINDOWS = object()

# The base charmworld API URL containing information about charms.
# This URL must be formatted with a series and a charm name.
CHARMWORLD_API = 'http://manage.jujucharms.com/api/3/charm/{series}/{charm}'

# The default Juju GUI charm URLs for each supported series. Used when it is
# not possible to retrieve the charm URL from the charmworld API, e.g. due to
# temporary connection/charmworld errors.
# Keep this list sorted by release date (older first).
DEFAULT_CHARM_URLS = collections.OrderedDict((
    ('precise', 'cs:precise/juju-gui-90'),
    ('trusty', 'cs:trusty/juju-gui-2'),
))

# The quickstart app short description.
DESCRIPTION = 'set up a Juju environment (including the GUI) in very few steps'

# The URL namespace for bundles in jujucharms.com.
JUJUCHARMS_BUNDLE_URL = 'https://jujucharms.com/bundle/'

# The path to the Juju command, based on platform.
JUJU_CMD_PATHS = {
    'default': '/usr/bin/juju',
    OSX: '/usr/local/bin/juju',
}

# Juju packages to install per platform.
JUJU_PACKAGES = {
    LINUX_APT: ('juju-core', 'juju-local'),
    OSX: ('juju', ),
}

# The possible values for the environments.yaml default-series field.
JUJU_DEFAULT_SERIES = ('precise', 'quantal', 'raring', 'saucy', 'trusty')

# Retrieve the current juju-core home.
JUJU_HOME = os.getenv('JUJU_HOME', '~/.juju')

# The name of the Juju GUI charm.
JUJU_GUI_CHARM_NAME = 'juju-gui'

# The name of the Juju GUI service.
JUJU_GUI_SERVICE_NAME = JUJU_GUI_CHARM_NAME

# The set of series supported by the Juju GUI charm.
JUJU_GUI_SUPPORTED_SERIES = tuple(DEFAULT_CHARM_URLS.keys())

# The minimum Juju GUI charm revision supporting bundle deployments, for each
# supported series. Assume not listed series to always support bundles.
MINIMUM_REVISIONS_FOR_BUNDLES = collections.defaultdict(
    lambda: 0, {'precise': 80})
