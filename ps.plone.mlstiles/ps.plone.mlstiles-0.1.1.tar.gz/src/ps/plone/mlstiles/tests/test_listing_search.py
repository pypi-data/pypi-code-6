# -*- coding: utf-8 -*-
"""Test Listing Search tile."""

# python imports
from mock import Mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from collective.cover.testing import ALL_CONTENT_TYPES
from collective.cover.tests.base import TestTileMixin
from plone.app.testing import (
    TEST_USER_ID,
    TEST_USER_NAME,
    login,
    setRoles,
)

# local imports
from ps.plone.mlstiles.testing import PS_PLONE_MLSTILES_INTEGRATION_TESTING
from ps.plone.mlstiles.tiles.listings import search


class ListingSearchTileTestCase(TestTileMixin, unittest.TestCase):
    """Validate the listing search tile."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    def setUp(self):
        super(ListingSearchTileTestCase, self).setUp()
        self.tile = search.ListingSearchTile(self.cover, self.request)
        self.tile.__name__ = u'ps.plone.mlstiles.listings.search'
        self.tile.id = u'test'

    def test_interface(self):
        """Validate the tile implementation."""
        self.interface = search.IListingSearchTile
        self.klass = search.ListingSearchTile
        super(ListingSearchTileTestCase, self).test_interface()

    def test_default_configuration(self):
        """Validate the default tile configuration."""
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        """Validate the accepted content types for the tile."""
        self.assertEqual(self.tile.accepted_ct(), ALL_CONTENT_TYPES)

    def test_tile_is_empty(self):
        """Validate that the tile is empty by default."""
        self.assertTrue(self.tile.is_empty())

    def test_delete_content(self):
        """Validate behavior when the content is removed."""
        obj = self.portal['my-collection']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertNotIn('form', rendered)

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        self.portal.manage_delObjects(['my-collection'])

        msg = 'Please drag&amp;drop some content here to populate the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())
