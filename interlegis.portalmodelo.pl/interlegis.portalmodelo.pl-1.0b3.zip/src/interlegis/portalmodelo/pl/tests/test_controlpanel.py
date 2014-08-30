# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.sync.controlpanel import ISyncSettings
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'sapl-sync-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@sapl-sync-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('sapl-sync', actions, 'control panel not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('sapl-sync', actions, 'control panel not removed')


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISyncSettings)

    def test_remote_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'remote'))
        self.assertEqual(self.settings.remote, '')

    def test_path_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'path'))
        self.assertEqual(self.settings.path, '')

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'interlegis.portalmodelo.pl.sync.controlpanel.ISyncSettings.'
        records = [
            BASE_REGISTRY + 'path',
            BASE_REGISTRY + 'remote',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
