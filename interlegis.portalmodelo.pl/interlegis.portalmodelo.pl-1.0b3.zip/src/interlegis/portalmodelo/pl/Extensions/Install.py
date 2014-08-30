# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.interfaces import ISAPLMenuItem
from plone import api
from zope.interface import noLongerProvides


def remove_marker_interface_and_layout(portal):
    if hasattr(portal, 'processo-legislativo'):
        if hasattr(portal['processo-legislativo'], 'parlamentares'):
            obj = portal['processo-legislativo']['parlamentares']
            if ISAPLMenuItem.providedBy(obj):
                noLongerProvides(obj, ISAPLMenuItem)
            if obj.getLayout() == '@@parliamentarians':
                obj.setLayout('folder_listing')


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_marker_interface_and_layout(portal)
        profile = 'profile-%s:uninstall' % PROJECTNAME
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
