# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from rt.maracas.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of rt.maracas into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rt.maracas is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('rt.maracas'))

    def test_uninstall(self):
        """Test if rt.maracas is cleanly uninstalled."""
        self.installer.uninstallProducts(['rt.maracas'])
        self.assertFalse(self.installer.isProductInstalled('rt.maracas'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IRtMaracasLayer is registered."""
        from rt.maracas.interfaces import IRtMaracasLayer
        from plone.browserlayer import utils
        self.failUnless(IRtMaracasLayer in utils.registered_layers())
