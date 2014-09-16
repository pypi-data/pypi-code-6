from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope import schema

class IMediaTypes(Interface):
    """
    Marks all Media types from Products.media*
    """

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    