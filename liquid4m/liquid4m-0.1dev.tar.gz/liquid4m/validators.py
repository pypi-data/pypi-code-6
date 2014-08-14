
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

from .exceptions import ValidationError
from functools import wraps

# func
def invalidateOnError( func ):

    """
    Decorator function to catch any exception during the isValid method.
    If any error occur it will return False automaticaly.
    """

    # bool
    def wrapper( self, element ):

        """
        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The given object is valid or not.
        @rtype: bool
        """

        try:
            return func( self, element )

        except:
            return False

    return wrapper

class Validator( object ):

    """
    Validator abstract class. All validator must be inherited from this class!
    Validators are responsible for validate the given field or fieldset information
    based on differenct conditions.
    """

    # Default error message if the validation fails
    msg = u''

    # void
    def __init__( self, msg = None ):

        """
        Constructor for Validator class. You can redefine the error message
        in this scope.

        @param msg: Error message
        @type msg: unicode
        """

        self.msg = msg or self.msg

    # dict
    def getData( self, element ):

        """
        Returns extra data for the error message.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Extra informations for the error message.
        @rtype: dict
        """

        return {}

    # unicode
    def getMessage( self, element ):

        """
        Create the final error message. Its convert the placeholders into name, label, 
        value information. 

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Final error message with all information
        @rtype: unicode
        """

        rdict = { k : ( unicode(v) if v is not None else u'-' ) for k,v in self.__dict__.items() }
        rdict.update({
            'name': element.getName(),
            'label': element.getLabel(),
            'value': unicode( element.getValue() )
        })
        rdict.update( self.getData( element ) )

        return self.msg % rdict

    # bool
    def isValid( self, element ):

        """
        Validate the given object. If you don't want to write your own
        exeception handling, please use the @invalidateOnError decorator
        to catch any exception and return False automaticaly.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: The given object is valid or not.
        @rtype: bool
        """

        raise RuntimeError(
            '%(cls)s.isValid( element ) is not implemented.' % {
                'cls': self.__class__.__name__ 
            }
        )

    # void
    def reformat( self, element ):

        """
        After the validation is over you can reformat the given value.
        You can use it for standardize some information.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        return

    # void
    def validate( self, element ):

        """
        Validate the given element. If an error is occur then it will
        raise a ValidationError with the final error message. Furthermore
        it will change the state of the element as well.

        After the validation is over its reformat the given value if its
        neccessary.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        if not self.isValid( element ):
            element.getState().setError( self.getMessage( element ) )
            raise ValidationError( element.getState().getError() )

        self.reformat( element )

class FieldSetValidator( Validator ):

    """
    Base class for FieldSet validation.
    """

    # void
    def __init__( self, position = None, field_names = None, msg = None ):

        """
        Base class for FieldSet validation.
        
        @param position: Field's name where the error message is shown
        @type position: unicode

        @param field_names: List of field names for the comparation
        @type field_names: list<unicode>

        @param msg: Error message if it fails
        @type msg: unicode
        """

        super( FieldSetValidator, self ).__init__( msg )

        self.field_names = field_names or []
        self.position = position

    # dict
    def getData( self, element ):

        """
        Returns extra data for the error message.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element

        @return: Extra informations for the error message.
        @rtype: dict
        """

        return {
            'labels': u', '.join([ element.getField( name ).getLabel() \
                for name in self.field_names ]),
            'names':  u', '.join( self.field_names ),
            'values':  u', '.join([ unicode( element.getField( name ).getValue() ) \
                for name in self.field_names ])
        }

    # void
    def validate( self, element ):

        """
        Validate the given element. If an error is occur then it will
        raise a ValidationError with the final error message. Furthermore
        it will change the state of the "position" element as well.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        if not self.isValid( element ):
            flashed_element = element \
                if self.position is None \
                else element.getField( self.position )

            flashed_element.getState().setError( self.getMessage( element ) )
            raise ValidationError( flashed_element.getState().getError() )

        self.reformat( element )


class Or( Validator ):

    """
    Validate the given element. If an error is raised by all of the 
    childrens it will delegate the last exception to the parent element.
    """

    # void
    def __init__( self, *args ):

        """
        Validate the given element. If an error is raised by all of the 
        childrens it will delegate the last exception to the parent element.
        
        @param args: List of validator objects
        @type args: list<validators.Validator>
        """

        super( Or, self ).__init__(u'')
        self.validators = args

    # bool
    def isValid( self, element ):

        """
        Validate the given element. If an error is raised by all of the 
        childrens it will delegate the last exception to the parent element.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        last_msg = None
        for validator in self.validators:
            try:
                validator.validate( element )
                if last_msg:
                    element.getState().setError(None)

                return True

            except ValidationError, e:
                last_msg = e.msg

        raise ValidationError( e.msg )

class And( Validator ):

    """
    Validate the given element. If an error is raised by the children 
    it will delegate this exception to the parent element.
    """

    # void
    def __init__( self, *args ):

        """
        Validate the given element. If an error is raised by the children 
        it will delegate this exception to the parent element.

        @param args: List of validator objects
        @type args: list<validators.Validator>
        """

        super( And, self ).__init__(u'')
        self.validators = args

    # bool
    def isValid( self, element ):

        """
        Validate the given element. If an error is raised by the children 
        it will delegate this exception to the parent element.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: form.Element
        """

        for validator in self.validators:
            validator.validate( element )

        return True
