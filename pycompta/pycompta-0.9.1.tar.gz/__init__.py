# -*- coding: utf-8 -*-

"""
Pycompta - Logilab - http://www.logilab.org - License is GPL 2
"""

import sys
import os.path as osp

from __pkginfo__ import version

L1 = 'ISO-8859-1'

# FIXME working around nasty bug
from mx.DateTime import Date, RelativeDateTime, DateTimeType, DateTimeDelta
import mx.DateTime

def myDateTime(*args):
    """mx.DateTime v3.0.0 has a nasty constructor bug"""

    date = mx.DateTime.Date(*args)
    if date.day == -1:
        date = mx.DateTime.Date(date.year, date.month, date.days_in_month)
    return date

last = Date(2007,1,-1)
if last.day != last.days_in_month:
    Date = myDateTime
# end FIXME

try: # FIXME required due to devtools
    from mx import DateTime
    DEBUT = DateTime.Date(0, 1, 1)
    FIN = DateTime.Date(9999, 12, -1)
except:
    pass


def absjoin(*parts):
    """
    return os.path.abspath(os.path.join(*parts))
    """
    return osp.abspath(osp.join(*parts))

def log(msg) :
    """
    Afficher message sur sortie standard
    """
    sys.stdout.write(msg)
    sys.stdout.flush()
