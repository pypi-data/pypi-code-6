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
__copyright__ = "Copyleft 2010 - Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

import lockflag
from lockflag import *

import os

def test_lockflag():

    dc = lockFlag(str(os.getpid()),'tmp')
    assert dc.create() == True
    assert os.path.exists(dc.fullpath) == True
    assert dc.exists() == True
    
    assert dc.create() == False
    
    dc.delete()
    assert dc.exists() == False
    

if __name__ == '__main__':
    import doctest
    import nose
    doctest.testmod()
    nose.main()