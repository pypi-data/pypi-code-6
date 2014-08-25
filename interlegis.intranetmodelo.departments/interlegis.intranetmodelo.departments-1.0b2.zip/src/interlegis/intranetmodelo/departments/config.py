# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts

from zope.interface import implements

PROJECTNAME = 'interlegis.intranetmodelo.departments'


class HiddenProducts(object):
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return [
            u'interlegis.intranetmodelo.departments.upgrades.v1010'
        ]


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.intranetmodelo.departments:uninstall',
            u'interlegis.intranetmodelo.departments.upgrades.v1010:default'
        ]
