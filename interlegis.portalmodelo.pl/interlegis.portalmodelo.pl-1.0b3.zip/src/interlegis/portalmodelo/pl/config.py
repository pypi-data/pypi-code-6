# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta

PROJECTNAME = 'interlegis.portalmodelo.pl'

# these constants must be date objects
NOW = date.today()
MAX_BIRTHDAY = NOW - timedelta(365 * 18)  # around 18 years back
MIN_BIRTHDAY = NOW - timedelta(365 * 100)  # around 100 years back
