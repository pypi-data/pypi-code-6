# -*- coding: utf-8 -*-
from pd.prenotazioni import prenotazioniLogger as logger


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-pd.prenotazioni:uninstall')
        logger.info("Uninstall done")
