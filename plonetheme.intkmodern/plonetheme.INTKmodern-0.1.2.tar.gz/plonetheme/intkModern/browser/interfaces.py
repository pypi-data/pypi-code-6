from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope import schema

"""
Base interfaces for further development and to adapt and extend theme
for particular websites
"""

class IMediaTypes(Interface):
    """
    Marks all Media types from Products.media*
    """

class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """
    