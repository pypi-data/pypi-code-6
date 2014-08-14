
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

from jinja2 import Environment, PackageLoader

class Widget( object ):

    """
    Base Widget class for interface rendering purposes.
    """

    # Default template path
    default_template = None

    # Default error widget for error message rendering
    default_error_widget = None

    # void
    def __init__( self, environment = None, template = None, html = None ):
        
        self._environment = environment or Environment(
            loader = PackageLoader('liquid4m')
        )
        self._html = html
        self._template = template or self.default_template
        self._error_widget = self.default_error_widget() \
            if self.default_error_widget is not None \
            else None

    # dict
    def getData( self ):

        return {}

    # unicode
    def getTemplate( self, element ):

        return self._template
    
    # void
    def setErrorWidget( self, error_widget ):

        self._error_widget = error_widget

    # Widget
    def getErrorWidget( self ):

        return self._error_widget  

    # unicode
    def render( self, element ):

        t = self._environment.get_template( self.getTemplate( element ) ) \
            if self._html is None \
            else self._environment.from_string( self._html )

        data = { 'e': element, 'error_widget': self.getErrorWidget() }
        data.update( self.getData() )
        return t.render( data )

class HTML( Widget ):

    pass

class FieldSet( Widget ):

    default_template = '_error_inline.jinja2'

    # unicode
    def getTemplate( self, element ):

        return 'fieldset.jinja2' \
            if element.getName() is not None \
            else 'block/fieldset.jinja2'

class TooltipError( Widget ):

    default_template = 'error/tooltip.jinja2'

class InlineError( Widget ):

    default_template = 'error/inline.jinja2'

class Form( Widget ):

    default_template = '_form.jinja2'

class Button( Widget ):

    default_template = '_button.jinja2'

    # void
    def __init__( self, label, name = None, url = None, is_primary = False, \
                  environment = None, template = None ):

        self.name = name
        self.label = label
        self.url = url
        self.is_primary = is_primary

        super( Button, self ).__init__( environment, template )

    # dict
    def getData( self ):

        return { 
            'name': self.name,
            'label': self.label,
            'url': self.url,
            'is_primary': self.is_primary
        }

class Input( Widget ):

    default_template = 'input.jinja2'
    default_error_widget = TooltipError

    # void
    def __init__( self, type, environment = None, template = None ):

        self.type = type.lower()
        super( Input, self ).__init__( environment, template )

    # dict
    def getData( self ):

        return { 'type': self.type }

class TextArea( Widget ):

    default_template = 'textarea.jinja2'
    default_error_widget = TooltipError

class Select( Widget ):

    default_template = 'select.jinja2'
    default_error_widget = TooltipError

class Checkbox( Widget ):

    default_template = 'checkbox.jinja2'
    default_error_widget = InlineError

class Radio( Widget ):

    default_template = 'radio.jinja2'
    default_error_widget = InlineError

