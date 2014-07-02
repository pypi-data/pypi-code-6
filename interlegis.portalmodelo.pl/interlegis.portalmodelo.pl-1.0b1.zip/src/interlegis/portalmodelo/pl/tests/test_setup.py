# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.interfaces import IBrowserLayer
from interlegis.portalmodelo.pl.testing import FUNCTIONAL_TESTING
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


PERMISSIONS = (
    'interlegis.portalmodelo.pl: Add Legislature',
    'interlegis.portalmodelo.pl: Add Parliamentarian',
    'interlegis.portalmodelo.pl: Add Session',
)


class Plone43TestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'interlegis.portalmodelo.pl:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.types = self.portal['portal_types']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']


class InstallTestCase(BaseTestCase):
    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_add_permissions(self):
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        for p in PERMISSIONS:
            roles = self.portal.rolesOfPermission(p)
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, expected)

    def test_parliamentarians_view_registered(self):
        folder_views = self.types['Folder'].view_methods
        self.assertIn('parliamentarians', folder_views)

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'1000',)
        )


class TestUpgrade(BaseTestCase):
    """Ensure product upgrades work."""

    def test_to1010_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('1010',))
                and (step[0]['source'] == ('1000',))]
        # upgrade step registration is being skiped for now
        self.assertEqual(len(step), 0)


class UninstallTestCase(BaseTestCase):
    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed_uninstalled(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    def test_parliamentarians_view_removed(self):
        folder_views = self.types['Folder'].view_methods
        self.assertNotIn('parliamentarians', folder_views)
