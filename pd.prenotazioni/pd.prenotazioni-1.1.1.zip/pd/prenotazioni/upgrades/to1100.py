 # -*- coding: utf-8 -*-
from plone import api
from pd.prenotazioni import prenotazioniLogger as logger
from rg.prenotazioni.interfaces import IPrenotazione
from transaction import commit

PROJECTNAME = 'pd.prenotazioni'
PROFILE_ID = 'profile-pd.prenotazioni:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            qi = api.portal.get_tool('portal_quickinstaller')
            p = qi.get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade(PROJECTNAME, '1100')
def reindex_prenotazione_searchble_text(context):
    ''' Read repository tool
    '''
    pc = api.portal.get_tool('portal_catalog')
    brains = pc(object_provides=IPrenotazione.__identifier__)
    total = len(brains)
    logger.info('Found %s objects to upgrade' % len(brains))
    done = 0
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=['SearchableText'])
        done += 1
        if done % 100 == 0:
            commit()
            logger.info('Progress %s/%s' % (done, total))
    logger.info("Reindexed SearchableText for inserzioni")

    commit()
    portal_setup = api.portal.get_tool('portal_setup')

    logger.info('Registering %s resources' % PROJECTNAME)
    portal_setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry', run_dependencies=False)  # noqa
    portal_setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry', run_dependencies=False)  # noqa
