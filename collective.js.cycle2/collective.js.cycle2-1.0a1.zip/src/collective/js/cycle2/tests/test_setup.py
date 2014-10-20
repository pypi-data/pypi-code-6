# -*- coding: utf-8 -*-
from collective.js.cycle2.interfaces import IAddOnInstalled
from collective.js.cycle2.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest

PROJECTNAME = 'collective.js.cycle2'

JS = [
    '++resource++collective.js.cycle2/jquery.cycle2.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.center.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IAddOnInstalled, registered_layers())

    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for js in JS:
            self.assertIn(js, resource_ids, js + ' not found on registry')


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IAddOnInstalled, registered_layers())

    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for js in JS:
            self.assertNotIn(js, resource_ids, js + ' found on registry')
