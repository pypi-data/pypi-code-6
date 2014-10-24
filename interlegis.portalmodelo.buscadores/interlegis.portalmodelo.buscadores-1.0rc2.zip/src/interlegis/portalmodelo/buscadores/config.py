# -*- coding: utf-8 -*-
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'interlegis.portalmodelo.buscadores'


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            u'interlegis.portalmodelo.buscadores.upgrades.v1010',
        ]

class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.portalmodelo.buscadores:uninstall',
            u'interlegis.portalmodelo.buscadores.upgrades.v1010:default'
        ]
