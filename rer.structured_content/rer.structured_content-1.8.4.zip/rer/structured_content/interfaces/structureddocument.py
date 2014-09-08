from Products.ATContentTypes.interfaces import ITextContent
from rer.structured_content.interfaces import IStructuredInterface


class IStructuredDocument(IStructuredInterface, ITextContent):
    """Description of the Example Type"""
