# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.interfaces import ISAPLMenuItem
from plone import api
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import directlyProvides
from zope.interface import implements

import logging

logger = logging.getLogger(PROJECTNAME)


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.portalmodelo.pl:uninstall',
            u'interlegis.portalmodelo.pl.upgrades.v1010:default'
        ]


def constrain_types(folder, addable_types):
    """Constrain addable types in folder.
    """
    folder.setConstrainTypesMode(1)
    folder.setImmediatelyAddableTypes(addable_types)
    folder.setLocallyAllowedTypes(addable_types)


def create_legislature_structure(site):
    """Create intranet structure.
    """
    logger.info(u'Criando estrutura da Legislatura')
    title = u'Processo Legislativo'
    description = u'Seção que contém as informações relacionadas à atividade legislativa, parlamentares, legislatura atual e anteriores.'
    folder = getattr(site, 'processo-legislativo', None)
    if folder is None:
        logger.debug(u'Criando pasta {0}'.format(title))
        obj = api.content.create(site, type='Folder', title=title)
        # XXX: following two lines are a workaround for issue in plone.api
        #      see: https://github.com/plone/plone.api/issues/99
        obj.setTitle(title)
        obj.setDescription(description)
        obj.reindexObject()
        folder = obj
    elif IFolderish.providedBy(folder):
        logger.debug(u'Pasta {0} existente; pulando criação'.format(title))
    else:
        raise RuntimeError(u'Impossivel criar a estrutura do processo legislativo')

    if api.content.get_state(folder) == 'private':
        api.content.transition(folder, 'publish')

    # TODO: deal with existing objects here also
    title = 'Parlamentares'
    description = u'Relação de parlamentares diplomados em cada legislatura.'
    obj = api.content.create(folder, type='Folder', title=title)
    obj.setTitle(title)
    obj.setDescription(description)
    obj.reindexObject()
    constrain_types(obj, 'Parliamentarian')
    # enable display menu item on this folder
    directlyProvides(obj, ISAPLMenuItem)
    obj.setLayout('@@parliamentarians')
    api.content.transition(obj, 'publish')

    title = 'Legislaturas'
    description = u'Relação de legislaturas e seus parlamentares, com as respectivas sessões legislativas.'
    obj = api.content.create(folder, type='Folder', title=title)
    obj.setTitle(title)
    obj.setDescription(description)
    obj.reindexObject()
    constrain_types(obj, 'Legislature')
    api.content.transition(obj, 'publish')

    title = 'Mesa Diretora'
    description = u'Membros da mesa diretora desta Casa Legislativa, relacionados por cada sessão legislativa.'
    obj = api.content.create(folder, type='Link', title=title, remoteUrl='../processo-legislativo/@@mesa-diretora')
    obj.setTitle(title)
    obj.setDescription(description)
    obj.reindexObject()
    api.content.transition(obj, 'publish')
    logger.debug(u'Estrutura criada e publicada')

    #title = 'Comissões'
    #description = u'Relação de comissões (permantentes, especiais, etc) desta Casa Legislativa.'
    #obj = api.content.create(folder, type='Folder', title=title)
    #obj.setTitle(title)
    #obj.setDescription(description)
    #obj.reindexObject()
    #api.content.transition(obj, 'publish')


def setup_various(context):
    marker_file = '{0}.txt'.format(PROJECTNAME)
    if context.readDataFile(marker_file) is None:
        return

    portal = api.portal.get()
    create_legislature_structure(portal)
