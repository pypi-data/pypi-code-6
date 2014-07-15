# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.mlstiles."""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility


PROFILE_ID = 'profile-ps.plone.mlstiles:default'


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Install ps.plone.mls
    * Add featured listings tile.
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    qi = getToolByName(site, 'portal_quickinstaller')

    qi.installProduct('ps.plone.mls')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
