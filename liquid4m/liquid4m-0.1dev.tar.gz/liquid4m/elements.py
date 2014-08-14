
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

from bisect import bisect
from . import state, widgets, exceptions, validators

class ElementBase( type ):

    """
    Base object of element (Field, FieldSet) managements in class level.
    After the initialization it will set the name of the field
    automatically.
    """

    # void
    def __new__( cls, name, bases, attrs ):

        """
        Base object of element (Field, FieldSet) managements in class level.
        After the initialization it will set the name of the field
        automatically.

        @param name: Name of the given class
        @type name: unicode

        @param bases: Base classes of the class
        @type bases: list<unicode>

        @param attrs: Attributes of the class
        @type attrs: dict
        """

        klass    = super( ElementBase, cls ).__new__( cls, name, bases, attrs )
        elements = []

        for key, value in attrs.items():

            # Do not touch with not Element attributes
            if not isinstance( value, Element ):
                continue

            # Set the name of the Element
            value.setName( key )

            # Collect them into a list for ordering purposes
            elements.insert( bisect( elements, value ), value )

        # Save the collected list
        klass._elements = elements
        return klass

class Element( object ):

    """
    Element abstract class.
    """

    # Default interface widget
    _default_widget = None

    # Default validators for the element
    _default_validators = []

    # Number of creation (used by ordering)
    _creation_counter = 0
 
    # void
    def __init__( self, name = None, label = None, hidden = False, \
                  required = False, readonly = False, disabled = False, \
                  focus = False, error = None, widget = None, \
                  validators = None, cls = None ):

        """
        Element abstract class.

        @param name: Element's name
        @type name: unicode

        @param label: Label of the element
        @type label: unicode

        @param hidden: Visibility of the element
        @type hidden: bool

        @param required: Require to fill out the element?
        @type required: bool

        @param readonly: Can you modify the element or it is readonly?
        @type readonly: bool

        @param disabled: Element is disabled for modification?
        @type disabled: bool

        @param focus: Is this the active element?
        @type focus: bool

        @param error: Current error message
        @type error: unicode

        @param widget: Widget object for rendering template
        @type widget: widgets.Widget

        @param validators: List of validator objects to check the element
        @type validators: list<validators.Validator>

        @param cls: Rendered HTML tag's class
        @type cls: unicode
        """

        # Save default variables
        self._creation_counter = Element._creation_counter
        self._cls = cls
        self._abs_name = None

        # Initialize a state.State object to handle State changes
        self._state = state.State( 
            required = required,
            hidden = hidden, 
            readonly = readonly, 
            disabled = disabled, 
            focus = focus,
            error = error,
        )

        # Save initialized parameters
        self._init = dict(
            label = label,
            hidden = hidden,
            widget = widget,
            validators = validators,
            cls = cls
        )

        # Set basic objects
        self.setWidget( widget )
        self.setValidators( validators )
        self.setName( name )
        self.setLabel( label )

        Element._creation_counter += 1

    # int
    def __cmp__( self, other ):

        """
        Determine the two element is the same or not.

        @param other: Other element
        @type other: elements.Element

        @return: Is it same or not
        @rtype: int
        """

        return cmp( self._creation_counter, other._creation_counter )

    # void
    def setName( self, name ):

        """
        Set the Element's name

        @param name: Element's new name
        @type name: unicode
        """

        self._name = name

    # void
    def setAbsName( self, parent_abs_name = None ):

        """
        Set the absolute name of the current Element. The absolute path
        is starting with the form.Form and determine a unique name for
        every field, based on the position of the element in the schema.

        @param parent_abs_name: Parent's absolute name
        @type parent_abs_name: unicode
        """

        self._abs_name = self.getName() \
            if parent_abs_name is None \
            else '{}_{}'.format( parent_abs_name, self.getName() )

    # void
    def setLabel( self, label ):

        """
        Set the element's label attribute.

        @param label: Element's new label
        @type label: unicode
        """

        self._label = label

    # void
    def setWidget( self, widget ):

        """
        Set the element's widget. Every element have a widget!
        If widget is not found It will give you WidgetExpectedError
        exception.

        @param widget: Element's widget object
        @type label: widgets.Widget
        """

        if isinstance( widget, widgets.Widget ):
            self._widget = widget

        if widget is not None:
            raise exceptions.WidgetExpectedError( self.__class__.__name__ )

        if self._default_widget is None:
            raise exceptions.WidgetExpectedError( self.__class__.__name__ )

        if len( self._default_widget ) == 1:
            self._widget = self._default_widget[0]()

        self._widget = self._default_widget[0]( *self._default_widget[1:] )

    # void
    def setErrorWidget( self, widget ):

        """
        Set the element's widget's error widget. Its responsible for
        how show the given error messages in the form.

        @param widget: Error widget object
        @type widget: widgets.Widget
        """

        self._widget.setErrorWidget( widget )

    # void
    def setValidators( self, validator_list ):

        """
        Set the element's validators. Its responsible for to check the given
        element.

        @param validator_list: List of validator objects
        @type validator_list: list<validator.Validator>
        """

        self._validators = []

        # Set the dafult validators
        if self._default_validators and isinstance( 
                self._default_validators, validators.Validator ):

            self._validators.append( self._default_validators )

        elif self._default_validators and isinstance( self._default_validators, 
                list ):

            self._validators += self._default_validators

        if validator_list is None:
            return

        # Set the given validators
        if isinstance( validator_list, validators.Validator ):
            self._validators += [ validator_list ]

        else:
            self._validators += validator_list

    # unicode
    def getID( self ):

        """
        Return an unique ID for the element based on the number of creation
        and the absolute name.

        @return: Unique ID
        @rtype: unicode
        """

        if self.getAbsName() is None:
            return None
        
        return '{}_{}'.format( self.getAbsName(), self._creation_counter )

    # unicode
    def getName( self ):

        """
        Returns the name of the element.

        @return: Name of the element.
        @rtype: unicode
        """

        return self._name

    # unicode
    def getAbsName( self ):

        """
        Returns the absolute name of the element.

        @return: Absolute name of the element.
        @rtype: unicode
        """

        return self._abs_name

    # unicode
    def getClass( self ):

        """
        Returns the HTML tag's classes.

        @return: TML tag's classes.
        @rtype: unicode
        """

        return self._cls

    # unicode
    def getLabel( self ):

        """
        Returns the label of the element.

        @return: Label of the element
        @rtype: unicode
        """

        return self._label

    # state.State
    def getState( self ):

        """
        Returns of the State object of the element. It contains the
        required, disabled, readonly, focus, error attributes.

        @return: State object
        @rtype: state.State
        """

        return self._state

    # list<validators.Validator>
    def getValidators( self ):

        """
        Returns the list of the selected validators.

        @return: List of validator objects
        @rtype: list<validators.Validator>
        """

        return self._validators

    # unicode
    def render( self ):

        """
        Render the element's. To create the rendering it will use the selected
        widget object.

        @return: HTML content of the element
        @rtype: unicode
        """

        return self._widget.render( self )

class ElementCollector( object ):

    """
    Element collector object. It could collect different Element objects
    in the class level to define the expected schema for the Form.
    """

    # ElementBase meta object to collect Elements.
    __metaclass__ = ElementBase

    # list<elements.Element>
    def getElements( self ):

        """
        Returns the registered list of elements.

        @return: List of elements.
        @rtype: list<elements.Element>
        """

        return self._elements

    # list<unicode>
    def getElementNames( self ):

        """
        Returns the registered elements name.

        @return: List of elements name.
        @rtype: list<unicode>
        """

        return [ r.getName() for r in self.getElements() ]

    # void
    def setErrorWidgets( self, widget ):

        """
        Set all element's error widget. Its responsible for
        how show the given error messages in the form.

        @param widget: Error widget object
        @type widget: widgets.Widget
        """

        self.setErrorWidget( widget )

        for element in self.getElements():
            element.setErrorWidget( widget )
