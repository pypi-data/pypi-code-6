# encoding: utf-8
# Copyright 2013 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

def prepareSites(portal):
    wfTool, catalog = getToolByName(portal, 'portal_workflow'), getToolByName(portal, 'portal_catalog')
    results = catalog(portal_type='Site')
    for site in [i.getObject() for i in results]:
        try:
            state = wfTool.getInfoFor(site, 'review_state')
            if state != 'published':
                wfTool.doActionFor(site, 'publish')
        except WorkflowException:
            # Fsck if I know why
            pass
        localRoles = site.get_local_roles()
        found = False
        for principal, roles in localRoles:
            if principal == 'AuthenticatedUsers':
                if u'Contributor' in roles:
                    found = True
                    break
        if not found:
            site.manage_setLocalRoles('AuthenticatedUsers', ['Contributor'])


def setupImportSteps(context):
    if context.readDataFile('edrnsite.vanity.marker.txt') is None: return
    portal = context.getSite()
    prepareSites(portal)
