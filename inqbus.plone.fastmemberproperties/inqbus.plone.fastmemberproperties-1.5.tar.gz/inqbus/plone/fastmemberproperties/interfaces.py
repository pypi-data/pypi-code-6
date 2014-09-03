
from zope import interface
import zope.component.interfaces

class IFastmemberpropertiesTool(interface.Interface):
    """
    """

class IMemberWillBeRemovedEvent(zope.component.interfaces.IObjectEvent):
    """A Plone member will be removed event"""