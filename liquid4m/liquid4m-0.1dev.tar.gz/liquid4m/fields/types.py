
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

import datetime, re
from dateutil import parser
from ..exceptions import TypeConversionError

class Type( object ):

    _default_types = []

    # bool
    def isInherited( self, value ):
        
        for checked_type in self._default_types:
            if isinstance( value, checked_type ):
                return True

        return False

    # type
    def convert( self, value ):

        raise RuntimeError( '%(cls)s.convert( value ) is not implemented!' % {
            'cls': self.__class__.__name__
        } )

    # type
    def modify( self, value ):

        return value

    # bool
    def isEmpty( self, value ):

        return ( value is None or len( unicode( value ).strip() ) == 0 )

    # type
    def getValue( self, value ):
        
        if self.isEmpty( value ):
            return None

        if self.isInherited( value ):
            return self.modify( value )
        
        try:
            return self.modify( self.convert( value ) )

        except:
            raise TypeConversionError()

class String( Type ):

    _default_types = [ unicode, str ]

    # unicode
    def convert( self, value ):

        return unicode( value )

    # unicode
    def modify( self, value ):

        return value.strip()

class Integer( Type ):
    
    _default_types = [ int ]

    # int
    def convert( self, value ):

        try:
            return int( value )

        except:
            return int( float( re.sub( r',', '.', value ) ) )

class Float( Type ):
    
    _default_types = [ float ]

    # float
    def _convert( self, value ):

        try:
            return float( value )

        except:
            return float( re.sub( r',', '.', value ) )

class Boolean( Type ):

    _default_types = [ bool ]

    # bool
    def convert( self, value ):

        if str( value ).lower() in ("yes", "y", "true",  "t", "1"): 
            return True

        if str( value ).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): 
            return False

        raise TypeError()

class Date( Type ):
            
    _default_types = [ datetime.date ]

    # datetime.date
    def parseString( self, value ):

        try:
            return parser.parse( value ).date()

        except:
            return parser.parse( value.split(' ')[0] ).date()

    # datetime.date
    def convert( self, value ):

        if isinstance( value, tuple ) or isinstance( value, list ):
            return datetime.date( value[0], value[1], value[2] )

        if isinstance( value, str ) or isinstance( value, unicode ):
            return self.parseString( value )

        if isinstance( value, datetime.datetime ):
            return value.date()

        raise TypeError()

class DateTime( Type ):
            
    _default_types = [ datetime.datetime ]

    # datetime.datetime
    def convert( self, value ):

        if isinstance( value, tuple ) or isinstance( value, list ):
            return datetime.datetime( value[0], value[1], value[2], value[3], value[4], value[5] )

        if isinstance( value, str ) or isinstance( value, unicode ):
            return parser.parse( value )

        if isinstance( value, datetime.date ):
            return datetime.datetime( value.year, value.month, value.day )

        raise TypeError()
