#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT: a jabber client
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013, 2014 Adrien Cossa (souliane@mailoo.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Configuration related useful methods """

from sat.core.log import getLogger
log = getLogger(__name__)

from sat.core.constants import Const as C
from sat.core.i18n import _

from ConfigParser import SafeConfigParser, DEFAULTSECT, NoOptionError, NoSectionError
from xdg import BaseDirectory
import os
import csv


def fixConfigOption(section, option, value, silent=True):
    """Force a configuration option value, writing it in the first found user
    config file, eventually creating a new user config file if none is found.

    @param section (str): the config section
    @param option (str): the config option
    @param value (str): the new value
    @param silent (boolean): toggle logging output (must be True when called from sat.sh)
    """
    config = SafeConfigParser()
    target_file = None
    for file_ in C.CONFIG_FILES[::-1]:
        # we will eventually update the existing file with the highest priority, if it's a user personal file...
        if not silent:
            log.debug(_("Testing file %s") % file_)
        if os.path.isfile(file_):
            if file_.startswith(os.path.expanduser('~')):
                config.read([file_])
                target_file = file_
            break
    if not target_file:
        # ... otherwise we create a new config file for that user
        target_file = BaseDirectory.save_config_path('sat') + '/sat.conf'
    if section and section.upper() != DEFAULTSECT and not config.has_section(section):
        config.add_section(section)
    config.set(section, option, value)
    with open(target_file, 'wb') as configfile:
        config.write(configfile)  # for the next time that user launches sat
    if not silent:
        if option in ('passphrase'):  # list here the options storing a password
            value = '******'
        log.warning(_("Config auto-update: %(option)s set to %(value)s in the file %(config_file)s") %
                    {'option': option, 'value': value, 'config_file': target_file})


def getConfig(config, section, name, default=None):
    """Get a configuration option

    @param config (SafeConfigParser): the configuration instance
    @param section (str): section of the config file (None or '' for DEFAULT)
    @param name (str): name of the option
    @param default (str): eventually default to this value, if not None
    @return: str, list or dict
    """
    if not section:
        section = DEFAULTSECT

    try:
        value = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        if default is None:
            raise e
        value = default

    if name.endswith('_path') or name.endswith('_dir'):
        value = os.path.expanduser(value)
    # thx to Brian (http://stackoverflow.com/questions/186857/splitting-a-semicolon-separated-string-to-a-dictionary-in-python/186873#186873)
    elif name.endswith('_list'):
        value = csv.reader([value], delimiter=',', quotechar='"').next()
    elif name.endswith('_dict'):
        value = dict(csv.reader([item], delimiter=':', quotechar='"').next()
                     for item in csv.reader([value], delimiter=',', quotechar='"').next())
    return value
