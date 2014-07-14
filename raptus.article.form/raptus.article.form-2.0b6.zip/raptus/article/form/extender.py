# -*- coding: utf-8 -*-
from Products.Archetypes.atapi import AnnotationStorage, BooleanField, BooleanWidget
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from raptus.article.core import RaptusArticleMessageFactory as _
from zope.component import adapts
from zope.interface import implements


class ExtensionBooleanField(ExtensionField, BooleanField):
    """ ExtensionBooleanField
    """

class FormFolderSchemaExtender(object):
    adapts(IPloneFormGenForm)
    implements(ISchemaExtender)

    fields = [
        ExtensionBooleanField('hideTitle',
            required = False,
            languageIndependent = True,
            default = True,
            storage = AnnotationStorage(),
            schemata = 'settings',
            accessor = 'HideTitle',
            widget = BooleanWidget(
                description='',
                label = _(u'label_hide_title', default=u'Hide title'),
                visible={'view' : 'hidden',
                         'edit' : 'visible'},
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
