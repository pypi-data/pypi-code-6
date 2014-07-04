#!/usr/bin/env python
###############################################################################
#                                                                             #
#    interface.py                                                             #
#                                                                             #
#    Container for maapping SQL-based commands to object-based interfaces     #
#                                                                             #
#     NO SQL TO BE SEEN ABOVE THIS LEVEL                                      #
#                                                                             #
#    Copyright (C) Michael Imelfort                                           #
#                                                                             #
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Michael Imelfort"
__copyright__ = "Copyright 2014"
__credits__ = ["Michael Imelfort"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Michael Imelfort"
__email__ = "mike@mikeimelfort.com"
__status__ = "Dev"

###############################################################################
###############################################################################
###############################################################################
###############################################################################

# system imports
import sqlite3 as lite

# local imports
from dancingPeasant.exceptions import *
from dancinPeasant.baseFile import BaseFile

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class Interface():
    """Class for implementing an interface to a SQL database"""
    def __init__(self, dbFileName, verbosity=0):
        self.dbFileName = dbFileName
        self.baseFile = BaseFile(verbosity=verbosity)

#------------------------------------------------------------------------------
# SQL WRAPPERS

    def simpleSelect(self,
                     columns,           # select these columns
                     table,             # from this table
                     condition=None,    # where these conditions are met
                     order=None         # order = ('col', ['ASC', 'DESC' or None])
                     ):
        """ wrap select statements comming in from the outside world

        columns: is an ordered list of column names in the table ['col1', 'col2', ... ] or ['*'] for all
        table: is a single string. EX: 'bob'
        condition: is a string which states the SQL condition. i.e. the part that comes after the where:

            "type='big' or color='red'"

        Note: the use of single quotes on the values. This is important.
        order is a string which dictates the ordering of the results. EX: 'col, asc'

        This function is a generator of rows.

        """
        pass

###############################################################################
###############################################################################
###############################################################################
###############################################################################
