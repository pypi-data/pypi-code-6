# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from pd.prenotazioni import prenotazioniLogger as logger

PROJECTNAME = 'pd.prenotazioni'
PROFILE_ID = 'profile-pd.prenotazioni:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            qi = getToolByName(context, 'portal_quickinstaller')
            p = qi.get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade(PROJECTNAME, '1010')
def add_new_profile(context):
    ''' Read repository tool
    '''
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'repositorytool')
    logger.info("New profile ha been added")
