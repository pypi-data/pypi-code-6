#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008 - Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

import timeflag
from timeflag import *

import os
import shutil

from test_common import *

flag_format = "%Y%m%d"
flag_dir = tests_dir
flag_name = "test_timeflag"
flag_extension = "dat"

timeflag_toupdate_name = "test_timeflag"
timeflag_toupdate_path = os.path.join(
                module_dir,
                flag_dir,
                '..',
                timeflag_toupdate_name + os.extsep + flag_extension)

def test_set():

    init_dir()

    dc = timeFlag(flag_dir, flag_name, flag_extension)
    now = now_str(flag_format)
    dc.setFormat(flag_format)
    assert dc.get() == now
    assert dc.getdiff() == (0, 0, 0, 0)
    assert dc.isuptodate() == True

def test_delete():

    init_dir()

    dc = timeFlag(flag_dir, flag_name, flag_extension)
    dc.update()
    assert os.path.exists(os.path.join(flag_dir, flag_name+os.extsep+flag_extension)) == True

    dc.delete()
    assert os.path.exists(os.path.join(flag_dir, flag_name+os.extsep+flag_extension)) == False

def test_update():

    init_dir()

    now = now_str(flag_format)
    assert os.path.exists(timeflag_toupdate_path) == True
    shutil.copy(timeflag_toupdate_path, flag_dir)
    assert os.path.exists(os.path.join(flag_dir, timeflag_toupdate_name+os.extsep+flag_extension)) == True

    dc = timeFlag(flag_dir, timeflag_toupdate_name, flag_extension)
    dc.setFormat(flag_format)

    dc.update()
    assert dc.get() == now

    dc.delete()
    assert os.path.exists(os.path.join(flag_dir, timeflag_toupdate_name+os.extsep+flag_extension)) == False


if __name__ == '__main__':
    import doctest
    import nose
    doctest.testmod()
    nose.main()
