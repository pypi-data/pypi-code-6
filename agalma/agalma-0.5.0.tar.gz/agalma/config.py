# Agalma - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of Agalma.
#
# Agalma is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agalma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agalma.  If not, see <http://www.gnu.org/licenses/>.

"""
Loads the Agalma configuration file into the BioLite configuration.
"""

import agalma
from biolite.config import *

prefix = agalma.__path__[0]
resources['agalma'] = prefix
parse(
	os.path.join(prefix, 'config', 'agalma.cfg'),
	'~/.biolite/agalma.cfg',
	*get_env_paths('AGALMA_CONFIG'))
parse_env_resources()

# vim: noexpandtab ts=4 sw=4
