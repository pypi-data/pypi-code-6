
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

class WidgetExpectedError( Exception ):

    """
    Raised when no Widget object is defined in the related Element.
    """

    pass

class TypeConversionError( Exception ):

    """
    Raised when the Element's setValue() function fails because of not
    valid value is arriving.
    """

    pass

class ValidationError( Exception ):

    """
    Raised when some validation condition fails. The exception will contains
    the message of the error.
    """

    # void
    def __init__( self, msg ):

        """
        Raised when some validation condition fails. The exception will 
        contains the message of the error.

        @param msg: Error message.
        @type msg: unicode
        """

        self.msg = msg

class ValidationCollectionError( Exception ):

    """
    Raised when some FieldSet validation condition fails. The exception will 
    contains all child's error message as well.
    """

    # void
    def __init__( self, errors ):

        """
        Raised when some FieldSet validation condition fails. The exception 
        will contains all child's error message as well.

        @param msg: Collected error messages.
        @type msg: list<tuple<unicode,unicode>>
        """

        self.errors = errors
