# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.mlstiles."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from ps.plone.mlstiles.testing import PS_PLONE_MLSTILES_INTEGRATION_TESTING


CSS = [
    '++resource++ps.plone.mlstiles/mlstiles.css',
]


class TestSetup(unittest.TestCase):
    """Validate setup process for ps.plone.mlstiles."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_product_is_installed(self):
        """Validate that our product is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('ps.plone.mlstiles'))

    def test_collective_cover_installed(self):
        """Validate that collective.cover is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('collective.cover'))

    def test_plone_mls_listing_installed(self):
        """Validate that plone.mls.listing is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.listing'))

    def test_ps_plone_mls_installed(self):
        """Validate that ps.plone.mls is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('ps.plone.mls'))

    def test_cssregistry(self):
        """Validate the CSS file registration."""
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_tiles_registered(self):
        """Validate that the tiles are registered."""
        registry = getUtility(IRegistry)
        key = 'plone.app.tiles'
        self.assertIn(
            'ps.plone.mlstiles.listings.collection',
            registry.records.get(key).value,
        )
        self.assertIn(
            'ps.plone.mlstiles.listings.recent',
            registry.records.get(key).value,
        )
        self.assertIn(
            'ps.plone.mlstiles.listings.search',
            registry.records.get(key).value,
        )

    def test_tiles_available(self):
        """Validate that the tiles are available within a cover."""
        registry = getUtility(IRegistry)
        key = 'collective.cover.controlpanel.ICoverSettings.available_tiles'
        self.assertIn(
            'ps.plone.mlstiles.listings.collection',
            registry.records.get(key).value,
        )
        self.assertIn(
            'ps.plone.mlstiles.listings.recent',
            registry.records.get(key).value,
        )
        self.assertIn(
            'ps.plone.mlstiles.listings.search',
            registry.records.get(key).value,
        )
