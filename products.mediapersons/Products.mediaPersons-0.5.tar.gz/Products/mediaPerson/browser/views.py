from Products.Five import BrowserView
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import FooterViewlet
from AccessControl import getSecurityManager
from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFCore.utils import getToolByName

class SocialButtonsView(ViewletBase):
    """
        Class for social buttons view
    """

