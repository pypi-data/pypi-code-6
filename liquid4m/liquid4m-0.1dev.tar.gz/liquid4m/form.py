
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

from . import widgets

# dict
def flattenAbsData( value_dict ):

    """
    Flat a multi-dimensional dictionary into one-dimensional dictionary.
    The keys will be concenated automatically.

    @param value_dict: Multi-dimensional dictionary
    @type value_dict: dict

    @return: One-dimensional dictionary
    @type: dict
    """

    r_dict = {}
    for key, value in ( value_dict or {} ).items():
        if not isinstance( value, dict ):
            r_dict[ key ] = value
            continue

        for ikey, ivalue in flattenAbsData( value ).items():
            r_dict[ u'{}_{}'.format( key, ikey ) ] = ivalue

    return r_dict

class Form( object ):

    """
    Form class to render HTML forms by Liquid.
    """

    # void
    def __init__( self, element, value = None, submit = u'Submit', \
                  buttons = None, cls = None ):

        """
        Form class to render HTML forms by Liquid. It requires an Element
        object and it will clone this element to create the form's basic
        element (we won't use the schema element).

        @param element: schema element object
        @type: elements.Element

        @param value: Initial value
        @type value: dict

        @param submit: Submit button's label
        @type submit: unicode

        @param buttons: list of Button widgets
        @type buttons: list<widgets.Button>

        @param cls: HTML class
        @type cls: unicode
        """

        # Clone the schema element
        self._element = element.clone()

        # Calculate abstract name for every child
        self._element.setAbsName()

        # Set the initial values
        self._element.setValue( value )

        # Add Submit button
        self._buttons = [ 
            widgets.Button( 
                submit,
                name = 'submit',
                is_primary = True 
            ) 
        ] + ( buttons or [] )

        # Define other variables
        self._widget = widgets.Form()
        self._cls = cls
        self.valid = None

    # elements.Element
    def __getattr__( self, attr ):

        """
        Form is working like a FieldSet, so you can use .attr to 
        returns an Element.

        @param attr: Attribute name
        @type attr: unicode

        @return: Field object
        @type: elements.Element
        """

        return getattr( self.getElement(), attr )

    # void
    def setErrorWidgets( self, widget ):

        """
        Set the element's widget's error widget. Its responsible for
        how show the given error messages in the form.

        @param widget: Error widget object
        @type widget: widgets.Widget
        """

        self.getElement().setErrorWidget( widget )

    # list<widgets.Button>
    def getButtons( self ):

        """
        Returns all buttons for the Form.

        @return: List of all button
        @rtype: list<widgets.Button>
        """

        return self._buttons

    # elements.Element
    def getElement( self ):

        """
        Returns basic element's clone.

        @return: Basic element
        @rtype: elements.Element
        """

        return self._element

    # unicode
    def getClass( self ):

        """
        Returns HTML class

        @return: HTML class
        @rtype: unicode
        """

        return self._cls

    # tuple<bool,list>
    def isValid( self, return_list = False ):

        """
        Checks the validity of the form's basic element.
        
        @param return_list: Returns list of error
        @type return_list: bool

        @return: Validity of the form
        @rtype: bool (or tuple<bool,list<tuple<unicode,unicode>>>)
        """

        if return_list:
            return self.getElement().isValid()

        valid, _ = self.getElement().isValid()
        self.valid = valid
        return valid

    # unicode
    def render( self ):

        """
        Render the form

        @return: HTML
        @rtype: unicode
        """

        return self._widget.render( self )

    # dict
    def getValue( self ):

        """
        Returns of the basic element's values

        @return: Element's values
        @rtype: dict
        """

        return self.getElement().getValue()

    # void
    def setValue( self, value ):

        """
        Set the values of the element.
        
        @param value: New values of the element
        @type value: dict
        """

        self.getElement().setValue( value )

    # void
    def delValue( self ):

        """
        Empty the element.
        """

        self.getElement().delValue()

    # Value property
    value = property( getValue, setValue, delValue )
