# -*- coding: utf-8 -*-

from zope.interface import alsoProvides
from redturtle.subsites import logger
from zope.publisher.skinnable import applySkin
from zope.component import getUtility 
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.component.interfaces import ComponentLookupError


# See also http://plone.293351.n2.nabble.com/changeSkin-method-behavior-on-Plone-4-2-for-applying-themes-td7561091.html
def setskin(site, event):
    """Eventhandler to set the skin"""
    skin_name = event.request.get('HTTP_PLONE_SKIN')
    portal_skins = site.portal_skins
    # only apply valid skins names
    if skin_name and skin_name in portal_skins.selections.keys():
        logger.debug("HTTP_PLONE_SKIN = %s" % skin_name)
        site.changeSkin(skin_name, event.request)
        # applySkin have a bad side-effect: it nullify all browserlayers interfaces
#        applySkin(event.request, skin_name)
        try:
            theme_interface = getUtility(IBrowserSkinType, name=skin_name)
            alsoProvides(event.request, theme_interface)
        except ComponentLookupError:
            pass
