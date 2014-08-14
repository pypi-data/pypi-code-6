
# -*- coding: utf-8 -*-

"""
Liquid is a form management tool for web frameworks.
Copyright (C) 2014, Bence Faludi (b.faludi@mito.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

# list<Option>
def generate( iterable ):

    rlist = []
    for item in iterable:
        if ( isinstance( item, list ) or isinstance( item, tuple ) ) and len( item ) >= 2:
            rlist.append( Option( item[0], item[1] ) )

        elif isinstance( item, dict ):
            rlist.append( Option( item.get('value'), item.get('label') ) )

    return rlist

class Option( object ):

    # void
    def __init__( self, value, label, disabled = False ):

        self._value = value
        self._label = label

    # unicode
    def getValue( self, element ):

        return element.getTypeValue( self._value )

    # unicode
    def getLabel( self ):

        return self._label

class Empty( Option ):

    # void
    def __init__( self, label = '-- Select --', disabled = False ):

        self._value = None
        self._label = label
