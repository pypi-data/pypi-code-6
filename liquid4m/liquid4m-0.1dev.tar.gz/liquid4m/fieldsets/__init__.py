
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

import inspect
from .. import widgets, form, exceptions, elements
from . import validators

class FieldSet( elements.Element, elements.ElementCollector ):

    _default_widget = widgets.FieldSet,

    # void
    def __init__( self, name = None, label = None, legend = None, cls = None, \
                  hidden = False, readonly = False, disabled = False, focus = False, \
                  error = None, type = None, widget = None, validators = None ):

        self._legend = legend
        super( FieldSet, self ).__init__( 
            name = name, 
            label = label,
            hidden = hidden, 
            required = False,
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
            widget = widget,
            validators = validators,
            cls = cls,
        )
        self._init.update( dict(
            legend = legend
        ) )

    # FieldSet
    def clone( self ):

        clone_dict = self._init
        clone_dict.update( self.getState().getState() )
        clone_dict['name'] = self.getName()

        init_args = set( list( 
            inspect.getargspec( self.__class__.__init__ ).args 
        ) )
        init_args.remove('self')

        fs = self.__class__(
            **{ k:v for k,v in clone_dict.items() if k in init_args }
        )

        fs._elements = []
        for element in self.getElements():
            clone = element.clone()
            fs._elements.append( clone )
            setattr( fs, clone.getName(), clone )

        return fs

    # void
    def setAbsName( self, parent_abs_name = None ):

        super( FieldSet, self ).setAbsName( parent_abs_name )

        for element in self.getElements():
            element.setAbsName( self.getAbsName() )

    # dict
    def _getValue( self ):

        return { element.getName() : element.getValue() for element in self.getElements() }

    # void
    def _setValue( self, value_dict ):

        for element in self.getElements():
            if isinstance( element, FieldSet ):
                element._setValue( value_dict )

            else:
                element.setValue( value_dict.get( element.getAbsName() ) )

    # Field
    def getField( self, name ):

        return getattr( self, name )

    # dict
    def getValue( self ):

        return self._getValue()

    # void
    def setValue( self, value_dict ):

        self._setValue( form.flattenAbsData( value_dict ) )

    # void
    def delValue( self ):

        self._setValue()

    value = property( getValue, setValue, delValue )

    # unicode
    def getLegend( self ):

        return self._legend

    # void
    def validate( self ):

        if not self.getState().isActive():
            return

        errors = []
        for element in self.getElements():
            success, error = element.isValid()
            errors += error

        for validator in self.getValidators():
            try:
                validator.validate( self )
            
            except exceptions.ValidationError, e:
                errors += [( self.getName(), e.msg )] 

        if len( errors ) != 0:
            raise exceptions.ValidationCollectionError( errors )

    # tuple<bool,list>
    def isValid( self ):

        try:
            self.validate()
            return True, []

        except exceptions.ValidationCollectionError, e:
            return False, e.errors

        except exceptions.ValidationError, e:
            return False, [ ( self.getName(), e.msg ) ]
