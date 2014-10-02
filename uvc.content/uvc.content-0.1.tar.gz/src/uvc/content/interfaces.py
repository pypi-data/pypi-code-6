# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import TextLine, Text


class IDescriptiveSchema(Interface):
    """A very basic descriptive schema.
    """
    title = TextLine(
        title=u"Title",
        required=True)

    description = Text(
        title=u'Description',
        required=False,
        default=u"")


class IContent(Interface):
    pass
