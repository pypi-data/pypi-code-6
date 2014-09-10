# -*- coding: utf-8 -*-
from pd.plonedemografico import plonedemograficoLogger as logger
from pd.plonedemografico.config import PROJECTNAME


def uninstall(portal, reinstall=False):
    ''' Run uninstall profile if needed
    '''
    if reinstall:
        return
    setup_tool = portal.portal_setup
    setup_tool.runAllImportStepsFromProfile(
        'profile-%s:uninstall' % PROJECTNAME
    )
    logger.info("Uninstall done")
