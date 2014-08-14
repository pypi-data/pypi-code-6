
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

class State( object ):

    """
    State object of given element. It knows the element is visible or
    required, or maybe in disabled status, etc.
    """

    # void
    def __init__( self, required, hidden, readonly, disabled, focus, error = None ):

        """
        State object of given element. It knows the element is visible or
        required, or maybe in disabled status, etc.

        @param required: Require to fill out the element?
        @type required: bool

        @param hidden: Visibility of the element
        @type hidden: bool

        @param readonly: Can you modify the element or it is readonly?
        @type readonly: bool

        @param disabled: Element is disabled for modification?
        @type disabled: bool

        @param focus: Is this the active element?
        @type focus: bool

        @param error: Current error message
        @type error: unicode
        """

        self.setError( error )
        self.setRequired( required )
        self.setHidden( hidden )
        self.setReadonly( readonly )
        self.setDisabled( disabled )
        self.setFocus( focus )

    # dict
    def getState( self ):

        """
        Returns the current state of the element.

        @return: Current state of the element
        @rtype: dict
        """

        return {
            'required': self.isRequired(),
            'readonly': self.isReadonly(),
            'focus': self.isFocus(),
            'disabled': self.isDisabled(),
            'hidden': self.isHidden(),
            'error': self.getError()
        }

    # void
    def setError( self, error ):

        """
        Set the error message of the field. This error message will be
        shown in the interface.

        @param error: Current error message
        @type error: unicode
        """

        self.error = error

     # void
    def setRequired( self, required = True ):

        """
        Set the required property of the element.

        @param required: Require to fill out the element?
        @type required: bool
        """

        self.required = required

    # void
    def setFocus( self, focus = True ):

        """
        Set the focus of the element.

        @param focus: Is this the active element?
        @type focus: bool
        """

        self.focus = focus

    # void
    def setHidden( self, hidden = True ):

        """
        Set the visibility of the element.
        
        @param hidden: Visibility of the element
        @type hidden: bool
        """

        self.hidden = hidden

    # void
    def setReadonly( self, readonly = True ):

        """
        Set the readonly property of the element.

        @param readonly: Can you modify the element or it is readonly?
        @type readonly: bool
        """

        self.readonly = readonly

    # void
    def setDisabled( self, disabled = True ):

        """
        Set the disabled property of the element.

        @param disabled: Element is disabled for modification?
        @type disabled: bool
        """

        self.disabled = disabled

    # bool
    def isError( self ):

        """
        Is any error message set? 

        @return: Is any error message set? 
        @rtype: bool
        """

        return self.error is not None

    # bool
    def isRequired( self ):

        """
        Is it required?

        @return: Is it required?
        @rtype: bool
        """

        return self.required

    # bool
    def isFocus( self ):

        """
        Is it in focus state?

        @return: Is it in focus state?
        @rtype: bool
        """

        return self.focus

    # bool
    def isHidden( self ):

        """
        Is it hidden?

        @return: Is it hidden?
        @rtype: bool
        """

        return self.hidden

    # bool
    def isReadonly( self ):

        """
        Is it readonly?

        @return: Is it readonly?
        @rtype: bool
        """

        return self.readonly

    # bool
    def isDisabled( self ):

        """
        Is it disabled?

        @return: Is it disabled?
        @rtype: bool
        """

        return self.disabled

    # bool
    def isActive( self ):

        """
        Is it active? We only need to validate those elements which
        are visible, not disabled and not readonly.

        @return: Is it active?
        @rtype: bool
        """

        if self.isHidden() or self.isReadonly() or self.isDisabled():
            return False

        return True

    # unicode
    def getError( self ):

        """
        Returns the error message.

        @return: Error message
        @rtype: unicode
        """

        return self.error
