from zope.interface import Interface


class IMobilethemeTwoLayer(Interface):
    """A layer specific to medialog.mobilethemeTwo
        """

from ZPublisher.interfaces import IPubStart
from zope.component import adapter
from zope.interface import alsoProvides

@adapter(IPubAfterTraversal)
def applyLayer(event):
    req = event.request
    if req.URL == 'http://localhost:8080/lin':
        alsoProvides(req, plone.app.theming.plugins.browserlayer.schemata.medialog.mobilethemeTwo)