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


import toolbox
from toolbox import *


def test_ensure_listindex():
    
    l = ( 'a', 'b', 'c' )
    assert ensure_listindex(l,'[0]') == 'a'    
    assert ensure_listindex(l, '[0][0]') == 'a'
    
    l = ( 0, 1, 2)
    assert ensure_listindex(l, '[0][0]', 3) == 3
    assert ensure_listindex(l, '[5]', 4) == 4

    
def test_logger_force_rollover():

    assert logger_force_rollover(logging.getLogger()) >= 0
    
    try:
        logger_force_rollover(None)
        logger_force_rollover(list())
    except Exception:
        assert False
    else:
        assert True

if __name__ == '__main__':
    
    import doctest
    doctest.testmod(toolbox)
    
    try:
        import nose
    except :
        pass
    else:
        nose.main()
