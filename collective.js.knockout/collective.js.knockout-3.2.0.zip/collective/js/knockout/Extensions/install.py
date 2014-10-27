# -*- coding: utf-8 -*-

from collective.js.knockout import logger


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.js.knockout:uninstall')
        logger.info("Uninstall done")
