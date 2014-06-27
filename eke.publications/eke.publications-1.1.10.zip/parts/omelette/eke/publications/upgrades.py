# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.CMFCore.utils import getToolByName
from eke.publications.interfaces import IPublicationFolder
from utils import setFacetedNavigation

def _getPortal(context):
    return getToolByName(context, 'portal_url').getPortalObject()

def nullUpgradeStep(setupTool):
    '''A null step for when a profile upgrade requires no custom activity.'''

def setUpFacetedNavigation(setupTool):
    '''Set up faceted navigation on all Publication Folders.'''
    portal = _getPortal(setupTool)
    request = portal.REQUEST
    catalog = getToolByName(portal, 'portal_catalog')
    results = [i.getObject() for i in catalog(object_provides=IPublicationFolder.__identifier__)]
    if len(results) == 0:
        # wtf? catalog must be out of date, because the common situation is that our EDRN
        # public portal does indeed have at least one Publication Folder
        if 'publications' in portal.keys():
            results = [portal['publications']]
    for pubFolder in results:
        setFacetedNavigation(pubFolder, request)
