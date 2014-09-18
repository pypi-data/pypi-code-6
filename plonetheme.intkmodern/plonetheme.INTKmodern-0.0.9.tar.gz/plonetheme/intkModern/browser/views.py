from plone.app.layout.viewlets.common import FooterViewlet
from AccessControl import getSecurityManager

class FooterView(FooterViewlet):
    """
    helper classes for footer
    """
    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True