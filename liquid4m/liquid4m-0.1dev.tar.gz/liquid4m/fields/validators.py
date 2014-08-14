
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

import re
from phonenumbers import is_valid_number, parse, format_number, PhoneNumberFormat
from validate_email import validate_email
from ..exceptions import ValidationError
from ..validators import *
from functools import wraps

class Required( Validator ):

    """
    Validate the given object's value. It will return success
    if the value is filled out.
    """

    # Default error message if the validation fails
    msg = u'Please fill out this field.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Validate the given object's value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element is empty or not.
        @rtype: bool
        """

        value = element.getValue()

        if isinstance( value, tuple ) or isinstance( value, list ) or isinstance( value, set ):
            return bool( value )

        return value is not None

class Compare( Validator ):

    """
    Compare the element's value based on different conditions.
    """

    # void
    def __init__( self, checked_value, comparable_value_fn = None, \
            comparable_attribute_fn = None, msg = None ):

        """
        Compare element's value based on different conditions.
        
        @param checked_value: The another value
        @type checked_value: type

        @param comparable_value_fn: Value function to check the comparable value
        @type comparable_value_fn: func

        @param comparable_attribute_fn: Attribute function which convert the 
            checked_value's value.
        @type comparable_attribute_fn: func

        @param msg: Error message
        @type msg: unicode
        """

        super( Compare, self ).__init__( msg )

        self.checked_value = checked_value

        if comparable_value_fn is not None:
            self._getComparableValue = comparable_value_fn

        if comparable_attribute_fn is not None:
            self._getComparableAttribute = comparable_attribute_fn

    # tyoe
    @staticmethod
    def _getComparableValue( compare_object, element ):

        """
        Returns the element's value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Element's value
        @rtype: type      
        """

        return element.getValue()

    # type
    @staticmethod
    def _getComparableAttribute( compare_object, element ):

        """
        Returns the checkable value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Checkable value
        @rtype: type      
        """

        return element.getTypeValue( compare_object.checked_value )

    # tyoe
    def getComparableValue( self, element ):

        """
        Returns the element's value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Element's value
        @rtype: type      
        """

        return getattr( self, '_getComparableValue' )( self, element )

    # type
    def getComparableAttribute( self, element ):

        """
        Returns the checkable value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Checkable value
        @rtype: type      
        """

        return getattr( self, '_getComparableAttribute' )( self, element )

    # dict
    def getData( self, element ):

        """
        Returns formatted checked_value for the error message.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: elements.Element

        @return: Extra data fields for error message.
        @rtype: dict
        """

        return {
            'boundary': unicode( self.getComparableAttribute( element ) ),
            'value': unicode( self.getComparableValue( element ) )
        }

class Equal( Compare ):

    """
    Checks element's value is not equal to an another value.
    """

    # Default error message if the validation fails
    msg = u'Value must be equal to %(boundary)s.'

     # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is equal to an another value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is equal to an another value.
        @rtype: bool
        """

        return self.getComparableValue( element ) == self.getComparableAttribute( element )

class NotEqual( Compare ):

    """
    Checks element's value is not equal to an another value.
    """

    # Default error message if the validation fails
    msg = u'Value must be not equal to %(boundary)s.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is not equal to an another value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is not equal to an another value.
        @rtype: bool
        """

        return self.getComparableValue( element ) != self.getComparableAttribute( element )

class Greater( Compare ):

    """
    Checks element's value is greater then or equal to an another value.
    """

    # Default error message if the validation fails
    msg = 'Value must be greater then or equal to %(boundary)s.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is greater then or equal to an another value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is greater then or equal to an another value.
        @rtype: bool
        """

        return self.getComparableValue( element ) >= self.getComparableAttribute( element )

class Less( Compare ):

    """
    Checks element's value is less then or equal to an another value.
    """

    # Default error message if the validation fails
    msg = 'Value must be less then or equal to %(boundary)s.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks element's value is less then or equal to an another value.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is less then or equal to an another value.
        @rtype: bool
        """

        return self.getComparableValue( element ) <= self.getComparableAttribute( element )

class Email( Validator ):

    """
    Checks the value is a valid email address or not.
    """

    # Default error message if the validation fails
    msg = u'Please enter a valid email address.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the value is a valid email address or not.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a valid email address
        @rtype: bool
        """

        return validate_email( element.getValue() )

class URL( Validator ):

    """
    Checks the value is a valid url or not.
    """
    
    # Default error message if the validation fails
    msg = u'Please enter an URL.'

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the value is a valid url or not.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a valid url
        @rtype: bool
        """

        regexp = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return regexp.match( element.getValue() ) is not None

class Telephone( Validator ):

    """
    Checks the value is a valid telephone number or not.
    """

    # Default error message if the validation fails
    msg = u'Please enter a telephone number.'

    # void
    def reformat( self, element ):

        """
        After the validation is over it convert to telephone number to E164
        format.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        prototype = parse( element.getValue(), element.getCountryCode() )
        element.setValue( format_number( prototype, PhoneNumberFormat.E164 ) )

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the value is a valid telephone number or not.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a telephone number
        @rtype: bool
        """

        prototype = parse( element.getValue(), element.getCountryCode() )
        return is_valid_number( prototype )

class Range( Validator ):

    """
    Checks the value between the given range.
    """

    # void
    def __init__( self, min_value = None, max_value = None, min_msg = None, \
                  max_msg = None, msg = None ):

        """
        Checks the value between the given range.

        @param min_value: Minimum value
        @type min_value: type

        @param max_value: Maximum value
        @type max_value: type

        @param min_msg: Error message for minimum value
        @type min_msg: unicode

        @param max_msg: Error message for maximum value
        @type max_msg: unicode

        @param msg: Global error message if it fails
        @type msg: unicode
        """

        super( Range, self ).__init__( msg )

        validators = []
        if min_value is not None:
            validators.append( Greater( min_value, msg = min_msg ) )

        if max_value is not None:
            validators.append( Less( max_value, msg = max_msg ) )

        self.validators = And( *validators )

    # bool
    def isValid( self, element ):

        """
        Checks the value between the given range.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a telephone number
        @rtype: bool
        """

        try:
            return self.validators.isValid( element )

        except ValidationError, e:
            if self.msg:
                return False

            raise ValidationError( e.msg )

class Length( Validator ):

    """
    Checks the value's length between the given range.
    """

    # Default error messages if the validation fails
    min_msg = 'Length must be greater then or equal to %(boundary)s.'
    max_msg = 'Length must be less then or equal to %(boundary)s.'

    # void
    def __init__( self, min_length = None, max_length = None, min_msg = None, \
                  max_msg = None, msg = None ):

        """
        Checks the value's length between the given range.

        @param min_length: Minimum value
        @type min_length: type

        @param max_length: Maximum value
        @type max_length: type

        @param min_msg: Error message for minimum value
        @type min_msg: unicode

        @param max_msg: Error message for maximum value
        @type max_msg: unicode

        @param msg: Global error message if it fails
        @type msg: unicode
        """

        super( Length, self ).__init__( msg )

        # int
        def getComparableValue( compare_object, element ):

            """
            Returns the element's length.

            @param compare_object: Compare validator object
            @type: validators.Compare

            @param element: Checked object (Field, FieldSet, etc.)
            @type: element.Element

            @return: Element's length
            @rtype: int
            """

            return len( element.getValue() )

        # int
        def getComparableAttribute( compare_object, element ):

            """
            Returns the boundary limit.

            @param compare_object: Compare validator object
            @type: validators.Compare

            @param element: Checked object (Field, FieldSet, etc.)
            @type: element.Element

            @return: Boundary limitation
            @rtype: int
            """

            return int( compare_object.checked_value )

        validators = []
        if min_length is not None:
            validators.append( 
                Greater( 
                    int( min_length ), 
                    msg = min_msg or self.min_msg,
                    comparable_attribute_fn = getComparableAttribute,
                    comparable_value_fn = getComparableValue
                ) 
            )

        if max_length is not None:
            validators.append( 
                Less( 
                    int( max_length ), 
                    msg = max_msg or self.max_msg,
                    comparable_attribute_fn = getComparableAttribute,
                    comparable_value_fn = getComparableValue
                ) 
            )

        self.validators = And( *validators )

    # bool
    def isValid( self, element ):

        """
        Checks the value's length between the given range.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a telephone number
        @rtype: bool
        """

        try:
            return self.validators.isValid( element )

        except ValidationError, e:
            if self.msg:
                return False

            raise ValidationError( e.msg )

class Pattern( Validator ):

    """
    Checks the pattern.
    """

    # Default error message if the validation fails
    msg = 'Please match the requested format.'

    # void
    def __init__( self, pattern, ignorecase = True, msg = None ):

        """
        Checks the pattern.

        @param pattern: Pattern to check
        @type pattern: unicode

        @param ignorecase: Ignorecase format is acceptable
        @type ignorecase: bool

        @param msg: Error message
        @type msg: unicode
        """

        self.pattern = pattern
        self._pattern = re.compile( self.pattern ) \
            if not ignorecase \
            else re.compile( pattern, re.I )

    # bool
    @invalidateOnError
    def isValid( self, element ):

        """
        Checks the pattern.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The element's value is a telephone number
        @rtype: bool
        """

        return self._pattern.match( element.getValue() ) is not None

class Selected( Length ):

    """
    Checks the selected items number in a given range.
    """
    
    # Default error messages if the validation fails
    min_msg = '%(value)s item is selected, it must be greater then or equal to %(boundary)s.'
    max_msg = '%(value)s item is selected, it must be less then or equal to %(boundary)s.'

    # void
    def __init__( self, min_selected = None, max_selected = None, \
                  min_msg = None, max_msg = None, msg = None ):

        """
        Checks the selected items number in a given range.

        @param min_length: Minimum value
        @type min_length: type

        @param max_length: Maximum value
        @type max_length: type

        @param min_msg: Error message for minimum value
        @type min_msg: unicode

        @param max_msg: Error message for maximum value
        @type max_msg: unicode

        @param msg: Global error message if it fails
        @type msg: unicode
        """

        super( Selected, self ).__init__( msg )

        # int
        def getComparableValue( compare_object, element ):

            """
            Returns the selected items number.

            @param compare_object: Compare validator object
            @type: validators.Compare

            @param element: Checked object (Field, FieldSet, etc.)
            @type: element.Element

            @return: Selected items number
            @rtype: int
            """

            return len( element.getValue() )

        # int
        def getComparableAttribute( compare_object, element ):

            """
            Returns the boundary limit.

            @param compare_object: Compare validator object
            @type: validators.Compare

            @param element: Checked object (Field, FieldSet, etc.)
            @type: element.Element

            @return: Boundary limitation
            @rtype: int
            """

            return int( compare_object.checked_value )

        validators = []
        if min_selected is not None:
            validators.append( 
                Greater( 
                    int( min_selected ), 
                    msg = min_msg or self.min_msg,
                    comparable_attribute_fn = getComparableAttribute,
                    comparable_value_fn = getComparableValue
                ) 
            )

        if max_selected is not None:
            validators.append( 
                Less( 
                    int( max_selected ), 
                    msg = max_msg or self.max_msg,
                    comparable_attribute_fn = getComparableAttribute,
                    comparable_value_fn = getComparableValue
                ) 
            )

        self.validators = And( *validators )
