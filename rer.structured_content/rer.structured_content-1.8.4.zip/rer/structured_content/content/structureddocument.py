# -*- coding: utf-8 -*-
"""Definition of the Structured Document content type
"""
from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute
from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from rer.structured_content.config import PROJECTNAME
from rer.structured_content.interfaces import IStructuredDocument
from zope.interface import implements
from ZPublisher.HTTPRequest import HTTPRequest

StructuredDocumentSchema = folder.ATFolderSchema.copy() + document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

StructuredDocumentSchema['title'].storage = atapi.AnnotationStorage()
StructuredDocumentSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    StructuredDocumentSchema,
    folderish=True,
    moveDiscussion=False
)

StructuredDocumentSchema['relatedItems'].widget.visible = {'view': 'visible', 'edit': 'visible'}


class StructuredDocument(folder.ATFolder):
    """Description of the Example Type"""
    implements(IStructuredDocument)

    meta_type = "Structured Document"
    schema = StructuredDocumentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()
    cmf_edit_kws = ('text_format',)

    security.declareProtected(View, 'CookedBody')
    def CookedBody(self, stx_level='ignored'):
        """CMF compatibility method
        """
        return self.getText()

    security.declareProtected(ModifyPortalContent, 'EditableBody')
    def EditableBody(self):
        """CMF compatibility method
        """
        return self.getRawText()

    security.declareProtected(ModifyPortalContent, 'setText')
    def setText(self, value, **kwargs):
        """Body text mutator

        * hook into mxTidy an replace the value with the tidied value
        """
        field = self.getField('text')

        # When an object is initialized the first time we have to
        # set the filename and mimetype.
        if not value and not field.getRaw(self):
            if 'mimetype' in kwargs and kwargs['mimetype']:
                field.setContentType(self, kwargs['mimetype'])
            if 'filename' in kwargs and kwargs['filename']:
                field.setFilename(self, kwargs['filename'])

        # hook for mxTidy / isTidyHtmlWithCleanup validator
        tidyOutput = self.getTidyOutput(field)
        if tidyOutput:
            value = tidyOutput

        field.set(self, value, **kwargs)  # set is ok

    text_format = ComputedAttribute(ATCTContent.getContentType, 1)

    security.declarePrivate('getTidyOutput')
    def getTidyOutput(self, field):
        """Get the tidied output for a specific field from the request
        if available
        """
        request = getattr(self, 'REQUEST', None)
        if request is not None and isinstance(request, HTTPRequest):
            tidyAttribute = '%s_tidier_data' % field.getName()
            return request.get(tidyAttribute, None)

atapi.registerType(StructuredDocument, PROJECTNAME)
