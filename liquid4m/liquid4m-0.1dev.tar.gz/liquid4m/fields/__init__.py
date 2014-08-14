
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

import types as t, inspect
from .. import widgets, form, exceptions, elements
from . import validators, types, options

class Field( elements.Element ):

    _default_type = None

    # void
    def __init__( self, name = None, value = None, label = None, placeholder = None, hint = None, \
                  hidden = False, readonly = False, disabled = False, focus = False, error = None, \
                  required = False, type = None, widget = None, validators = None, cls = None ):

        self._placeholder = placeholder
        self._hint = hint
        self._type = type or self._default_type()

        self.setValue( value )

        super( Field, self ).__init__( 
            name = name, 
            label = label,
            hidden = hidden, 
            required = required,
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
            widget = widget,
            validators = validators,
            cls = cls,
        )

        self._init.update( dict(
            placeholder = placeholder,
            hint = hint,
            type = type
        ) )

    # Field
    def clone( self ):

        clone_dict = self._init
        clone_dict.update( self.getState().getState() )
        clone_dict['value'] = self.getValue()
        clone_dict['name'] = self.getName()

        init_args = set( list( 
            inspect.getargspec( self.__class__.__init__ ).args 
        ) )
        init_args.remove('self')

        return self.__class__(
            **{ k:v for k,v in clone_dict.items() if k in init_args }
        )

    # void
    def validate( self ):

        if not self.getState().isActive():
            return

        if self.getState().isRequired():
            validators.Required().validate( self )

        if self.getValue() is None:
            return

        for validator in self.getValidators():
            validator.validate( self )

    # tuple<bool,list>
    def isValid( self ):

        try:
            self.validate()
            return True, []

        except exceptions.ValidationError, e:
            return False, [( self.getName(), e.msg )]

    # void
    def _setValue( self, value ):

        self._value = self.getTypeValue( value )

    # type
    def _getValue( self ):

        return self._value

    # type
    def getValue( self ):

        return self._getValue()

    # void
    def setValue( self, value ):

        self._setValue( value )

    # void
    def delValue( self ):

        self._setValue( None )

    value = property( getValue, setValue, delValue )

    # unicode
    def getPlaceholder( self ):

        return self._placeholder

    # type
    def getTypeValue( self, value ):

        return self._type.getValue( value )

    # unicode
    def getHint( self ):

        return self._hint

class Text( Field ):

    _default_widget = widgets.Input, 'text'
    _default_type = types.String

class Hidden( Field ):

    _default_widget = widgets.Input, 'hidden'
    _default_type = types.String

class Password( Field ):

    _default_widget = widgets.Input, 'password'
    _default_type = types.String

class Search( Field ):

    _default_widget = widgets.Input, 'search'
    _default_type = types.String

class Email( Field ):

    _default_widget = widgets.Input, 'email'
    _default_type = types.String
    _default_validators = validators.Email()

class Telephone( Field ):

    _default_widget = widgets.Input, 'tel'
    _default_type = types.String
    _default_validators = validators.Telephone()

    # void
    def __init__( self, name = None, value = None, label = None, placeholder = None, hint = None, \
                  hidden = False, readonly = False, disabled = False, focus = False, error = None, \
                  required = False, type = None, widget = None, validators = None, cls = None, \
                  country_code = None ):

        self._country_code = country_code

        super( Telephone, self ).__init__( 
            name = name, 
            value = value,
            label = label,
            placeholder = placeholder,
            hint = hint,
            hidden = hidden, 
            required = required,
            readonly = readonly, 
            disabled = disabled,
            error = error, 
            focus = focus,
            type = type,
            widget = widget,
            validators = validators,
            cls = cls,
        )

        self._init.update( dict(
            country_code = country_code
        ) )

    # unicode
    def getCountryCode( self ):

        return self._country_code

class URL( Field ):

    _default_widget = widgets.Input, 'url'
    _default_type = types.String
    _default_validators = validators.URL()

class TextArea( Field ):

    _default_widget = widgets.TextArea,
    _default_type = types.String

class Number( Field ):

    _default_widget = widgets.Input, 'number'
    _default_type = types.Integer

class Year( Field ):

    _default_widget = widgets.Input, 'number'
    _default_type = types.Integer
    _default_validators = validators.Range( 1900, 2100 )

class Date( Field ):

    _default_widget = widgets.Input, 'date'
    _default_type = types.Date

class DateTime( Field ):

    _default_widget = widgets.Input, 'datetime'
    _default_type = types.DateTime

class Select( Field ):

    _default_widget = widgets.Select, 
    _default_type = types.String

    # void
    def __init__( self, options, name = None, value = None, label = None, type = None, \
                  multiple = False, placeholder = None, hint = None, hidden = False, \
                  readonly = False, disabled = False, focus = False, required = False, \
                  error = None, widget = None, validators = None, cls = None ):

        self.setOptions( options )
        self._multiple = multiple

        super( Select, self ).__init__( 
            name = name, 
            value = value,
            label = label,
            placeholder = placeholder,
            hint = hint,
            hidden = hidden, 
            required = required,
            readonly = readonly, 
            disabled = disabled,
            error = error, 
            focus = focus,
            type = type,
            widget = widget,
            validators = validators,
            cls = cls,
        )

        self._init.update( dict(
            options = options,
            multiple = multiple
        ) )

        if self.isMultiple():
            self._widget.setErrorWidget( widgets.InlineError() )

    # bool
    def isMultiple( self ):

        return self._multiple

    # void
    def setOptions( self, options ):

        self._options = options

    # list<Option>
    def getOptions( self, *args ):

        if isinstance( self._options, list ) or type( self._options ).__name__ == 'generator':
            return self._options

        return self._options( *args )

    # void
    def _setValue( self, value ):

        if not self.isMultiple():
            self._value = self.getTypeValue( value )
            return

        if isinstance( value, list ) or isinstance( value, set ) or isinstance( value, tuple ): 
            self._value = { self.getTypeValue( v ) for v in value }
            return

        try:
            if self.getTypeValue( value ) is not None:
                self._value = { self.getTypeValue( value ) }
                return

        except:
            pass
        
        self._value = set([])

class Checkbox( Select ):

    _default_widget = widgets.Checkbox, 

    # void
    def __init__( self, options, name = None, value = None, label = None, type = None, \
                  placeholder = None, hint = None, hidden = False, \
                  readonly = False, disabled = False, focus = False, required = False, \
                  error = None, widget = None, validators = None, cls = None ):

        super( Checkbox, self ).__init__( 
            name = name, 
            options = options,
            value = value,
            label = label,
            multiple = True,
            placeholder = placeholder,
            hint = hint,
            hidden = hidden, 
            required = required,
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
            type = type,
            widget = widget,
            validators = validators,
            cls = cls,
        )

class SwitchCheckbox( Checkbox ):

    _default_type = types.Boolean

    # void
    def __init__( self, option, name = None, value = None, label = None, \
                  placeholder = None, hint = None, hidden = False, \
                  readonly = False, disabled = False, focus = False, \
                  error = None, widget = None, validators = None, cls = None ):

        super( Checkbox, self ).__init__( 
            name = name, 
            options = [ option ],
            value = value,
            label = label,
            multiple = False,
            placeholder = placeholder,
            hint = hint,
            hidden = hidden, 
            required = False,
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
            type = None,
            widget = widget,
            validators = validators,
            cls = cls,
        )
        self._init.update({
            'option': option
        })

    # void
    def _setValue( self, value ):

        self._value = self.getTypeValue( value ) or False

class Radio( Select ):

    _default_widget = widgets.Radio, 

    # void
    def __init__( self, options, name = None, value = None, label = None, type = None, \
                  placeholder = None, hint = None, hidden = False, \
                  readonly = False, disabled = False, focus = False, required = False, \
                  error = None, widget = None, validators = None, cls = None ):

        super( Radio, self ).__init__( 
            name = name, 
            options = options,
            value = value,
            label = label,
            multiple = False,
            placeholder = placeholder,
            hint = hint,
            hidden = hidden, 
            required = required,
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
            type = type,
            widget = widget,
            validators = validators,
            cls = cls,
        )

