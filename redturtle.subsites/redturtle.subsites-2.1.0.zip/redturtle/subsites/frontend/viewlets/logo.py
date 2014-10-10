# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.common import LogoViewlet as BaseLogoViewlet

class LogoViewlet(BaseLogoViewlet):
    """Customized version of the logo viewlet, where the logo URL is taken from the subsite"""

    def update(self):
        super(LogoViewlet, self).update()

        portal_url = self.portal_state.portal_url()
        
        # Commonly is '<img src="http://host/logo.png" alt="" title="" height="x" width="y" />'
        self.logo_tag = self.logo_tag.replace(portal_url, self.navigation_root_url)

        # BBB: is ok keeping the main site name?
        #self.portal_title = self.portal_state.portal_title()

