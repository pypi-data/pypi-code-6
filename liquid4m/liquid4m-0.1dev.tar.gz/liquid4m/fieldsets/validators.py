
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

from ..validators import *

class Same( FieldSetValidator ):

    """
    Check the difference between given fields.
    """

    # Default error message if the validation fails
    msg = u'%(labels)s values have to be the same!'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Check the difference between given fields.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The fields are the same?
        @rtype: bool
        """

        return len({ element.getField( name ).getValue() for name in self.field_names }) == 1

class Different( FieldSetValidator ):

    """
    Check the difference between given fields.
    """

    # Default error message if the validation fails
    msg = u'%(labels)s values have to be different!'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Check the difference between given fields.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The fields are different?
        @rtype: bool
        """

        return len({ element.getField( name ).getValue() for name in self.field_names }) == len( self.field_names )

class Compare( FieldSetValidator ):

    """
    Base comparation FieldSet validator.
    """

    # Allow equals
    equal = False

    # void
    def __init__( self, position, field_name, other_field_name, msg = None ):

        """
        Base comparation FieldSet validator.
        
        @param position: Field's name where the error message is shown
        @type position: unicode

        @param field_name: Field name
        @type field_name: unicode

        @param other_field_name: Field name
        @type other_field_name: unicode

        @param equal: In the comparation we allow equals or not
        @type equal: bool

        @param msg: Error message if it fails
        @type msg: unicode
        """

        super( Compare, self ).__init__( 
            position, 
            [ field_name, other_field_name ], 
            msg 
        )

        self.field_name = field_name
        self.other_field_name = other_field_name

    # dict
    def getData( self, element ):

        """
        Returns extra data for the error message.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Extra informations for the error message.
        @rtype: dict
        """

        v1 = element.getField( self.field_name ).getValue()
        v2 = element.getField( self.other_field_name ).getValue()

        l1 = element.getField( self.field_name ).getLabel()
        l2 = element.getField( self.other_field_name ).getLabel()

        rdict = super( Compare, self ).getData( element )
        rdict.update({
            'field_value': unicode( v1 ),
            'other_field_value': unicode( v2 ),
            'field_label': l1,
            'other_field_label': l2
        })

        return rdict

class Greater( Compare ):

    """
    Checks element's value is greater then an another element's
    value.
    """

    # Default error message if the validation fails
    msg = u'%(field_label)s must be greater then %(other_field_value)s.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is greater to an another element's
        value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is greater then or equal to an another 
            element's value.
        @rtype: bool
        """

        v1 = element.getField( self.field_name ).getValue()
        v2 = element.getField( self.other_field_name ).getValue()

        if not v1 or not v2:
            return True

        return v1 >= v2 \
            if self.equal \
            else v1 > v2

class GreaterAndEqual( Greater ):

    """
    Checks element's value is greater and equal then an another element's
    value.
    """

    # Default error message if the validation fails
    msg = u'%(field_label)s must be greater then or equal to %(other_field_value)s.'

    # Allow equals
    equal = True

class Less( Compare ):

    """
    Checks element's value is less then an another element's
    value.
    """

    # Default error message if the validation fails
    msg = u'%(field_label)s must be less then %(other_field_value)s.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is less then an another element's
        value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is less then an another
            element's value.
        @rtype: bool
        """

        v1 = element.getField( self.field_name ).getValue()
        v2 = element.getField( self.other_field_name ).getValue()

        if not v1 or not v2:
            return True

        return v1 <= v2 \
            if self.equal \
            else v1 < v2

class LessAndEqual( Less ):

    """
    Checks element's value is less and equal then an another element's
    value.
    """

    # Default error message if the validation fails
    msg = u'%(field_label)s must be less then or equal to %(other_field_value)s.'

    # Allow equals
    equal = True

class NoneOf( FieldSetValidator ):

    """
    Checks the FieldSet has any value filled out.
    """

    # Default error message if the validation fails
    msg = u'Please do not fill out this block.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the FieldSet has any value filled out.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: FieldSet has any value filled out.
        @rtype: bool
        """

        for name in self.field_names or element.getElementNames():
            if element.getField( name ).getValue():
                return False

        return True

class AnyOf( FieldSetValidator ):

    """
    FieldSet has any value filled out.
    """

    # Default error message if the validation fails
    msg = u'Please fill out at least one field.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the FieldSet has any value filled out.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: FieldSet has any value filled out.
        @rtype: bool
        """

        for name in self.field_names or element.getElementNames():
            if element.getField( name ).getValue():
                return True

        return False

class AllOf( FieldSetValidator ):

    """
    Checks the FieldSet has all of the fields filled out.
    """

    # Default error message if the validation fails
    msg = u'Please fill out all of the fields.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the FieldSet has all of the fields filled out.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: FieldSet has all of the fields filled out.
        @rtype: bool
        """

        for name in self.field_names or element.getElementNames():
            if not element.getField( name ).getValue():
                return False

        return True

