# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from Products.PloneFormGen.widgets.fieldset import FieldsetStartWidget as BaseWidget

class FieldsetStartWidget(BaseWidget):
    '''Pseudo widget that starts an XHTML fieldset.'''
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': 'widget_url_fieldset_start',
        'show_legend': True
    })
    
registerWidget(
    FieldsetStartWidget,
    title='URL fieldset start widget',
    description=('Renders XHTML fieldset open tag and displays URL to a page to review',),
    used_for=('eke.review.content.urlfieldsetfolder.URLFieldsetFolder',)
)
