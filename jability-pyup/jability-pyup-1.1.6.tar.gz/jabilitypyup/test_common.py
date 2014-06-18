#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2010 ROMAND Fabrice <fabrom@jability.org>
#
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

import datetime
import os
import shutil
import time

module_dir = os.path.dirname(__file__)
tests_dir = os.path.join(module_dir, 'tests/temp/')
test_filename_template = 'test_%d.tmp'
test_qty = 10


def now():
    return datetime.datetime.now()

def now_str(format="%Y%m%d%H%M%S"):
    return now().strftime(format)

def def_times(qty, daytimedelta=True):
    today = now()
    tlist = list()
    if daytimedelta:
        for i in range(qty):
            pastday = today - datetime.timedelta(days=i)
            atime = int(time.mktime(pastday.timetuple()))
            mtime = atime
            times = (atime,mtime)
            tlist.append(times)
    else:
        for i in range(qty):
            pastday = today - datetime.timedelta(minutes=i*5)
            atime = int(time.mktime(pastday.timetuple()))
            mtime = atime
            times = (atime,mtime)
            tlist.append(times)        
    return tlist

def init_dir(daydelta=True):
    shutil.rmtree(tests_dir)
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)
    i = 0
    flist = list()
    for times in def_times(test_qty, daydelta):
        fpath = os.path.join(tests_dir, test_filename_template % (i))
        open(fpath,'w').close()
        os.utime(fpath, times)
        i += 1
        flist.append(fpath)
    return flist

def clean_dir(flist, delete_base_dir=False):
    for file in flist:
        if os.path.exists(file):
            os.remove(file)
    if delete_base_dir:
        os.rmdir(tests_dir)

def count_existing_files(flist):
    i = 0
    for file in flist:
        if os.path.exists(file):
            i += 1
    return i


def test_tests_functions():

    files = init_dir()
    assert count_existing_files(files) == test_qty
    clean_dir(files)
    assert count_existing_files(files) == 0


if __name__ == '__main__':
    import doctest
    import nose
    doctest.testmod()
    nose.main()
