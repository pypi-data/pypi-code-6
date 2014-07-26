# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2014 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

"""
Time Utilities
"""

from __future__ import unicode_literals

import datetime

import pytz


def localtime(config, time=None, key='default'):
    """
    Return a datetime which has been localized to a particular timezone.

    :param config: Reference to a configuration object.

    :param time: Optional datetime instance to be localized.  If not provided,
       the current time ("now") is assumed.

    :param key: Config key to be used in determining to which timezone the time
       should be localized.
    """
    zone = timezone(config, key)
    if time is None:
        time = datetime.datetime.utcnow()
        time = pytz.utc.localize(time)
        time = zone.normalize(time.astimezone(zone))
    else:
        time = zone.localize(time)
    return time


def timezone(config, key='default'):
    """
    Return a timezone object based on the definition found in config.

    :param config: Reference to a config object.

    :param key: Config key used to determine which timezone should be returned.
    """
    zone = config.require('rattail', 'timezone.{0}'.format(key))
    return pytz.timezone(zone)
