# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.review import config
from eke.review import ProjectMessageFactory as _
from eke.review.interfaces import IURLFieldsetFolder
from eke.review.widgets import FieldsetStartWidget
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View
from Products.PloneFormGen.content import fieldset
from zope.interface import implements

URLFieldsetFolderSchema = fieldset.FieldsetFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'destinationURL',
        required=True,
        searchable=False,
        default=u'http://',
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_(u'Destination URL'),
            description=_(u'Enter the URL of the link to display in this field set. The URL will open in a new window.'),
        ),
    ),
    atapi.StringField(
        'urlLabel',
        required=False,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u'URL Label'),
            description=_(u'Label for the URL above. If not given, the URL itself will be displayed.'),
        ),
    ),
))

class URLFieldsetFolder(fieldset.FieldsetFolder):
    '''A fieldset that also has a URL.'''
    implements(IURLFieldsetFolder)
    schema          = URLFieldsetFolderSchema
    meta_type       = portal_type = 'URLFieldsetFolder'
    archetype_name  = 'URL Fieldset Folder'
    typeDescription = 'A fieldset with a clickable URL preceeding all the fields.'
    def __init__(self, oid, **kwargs):
        '''Initializer for a URLFieldsetFolder'''
        super(URLFieldsetFolder, self).__init__(oid, **kwargs)
        self.fsStartField = atapi.StringField(
            'FieldsetStart',
            searchable=False,
            required=False,
            write_permission=View,
            widget=FieldsetStartWidget(),
        )
    def setDestinationURL(self, value, **kw):
        self.fsStartField.widget.destinationURL = self.destinationURL = value
    def setUrlLabel(self, value, **kw):
        if not value:
            self.fsStartField.widget.urlLabel = self.urlLabel = None
        else:
            self.fsStartField.widget.urlLabel = self.urlLabel = value

registerATCT(URLFieldsetFolder, config.PROJECTNAME)
