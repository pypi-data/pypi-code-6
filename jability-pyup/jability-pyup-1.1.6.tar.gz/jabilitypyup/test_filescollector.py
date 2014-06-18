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


import filescollector
from filescollector import *

import os

import test_common

def test_clean_olders():

    files = test_common.init_dir()
    assert test_common.count_existing_files(files) == test_common.test_qty

    fcollector = FilesCollector()
    fcollector.setSourceDir(test_common.tests_dir)
    fcollector.setFileFilter(r'^.*\.tmp$')
    files = fcollector.run(True)
    assert test_common.count_existing_files(files) == test_common.test_qty

    test_common.clean_dir(files)
    assert test_common.count_existing_files(files) == 0


def test_minimumFileAge():
    
    files = test_common.init_dir(False)
    assert test_common.count_existing_files(files) == test_common.test_qty
    
    fcollector = FilesCollector()
    fcollector.setSourceDir(test_common.tests_dir)
    fcollector.setFileFilter(r'^.*\.tmp$')
    fcollector.setMinimumFileLastChangeAge(15)
    files = fcollector.run(True)
    assert test_common.count_existing_files(files) == 7
    
    test_common.clean_dir(files)
    

if __name__ == '__main__':
    import doctest
    import nose
    doctest.testmod(filescollector)
    nose.main()
