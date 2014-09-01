# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.contactauthor import logger


PROFILE_ID = 'profile-collective.contactauthor:default'

def migrateTo2000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'browserlayer')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'controlpanel')
    logger.info('Migrated to version 1.1')
