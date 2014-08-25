# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.interfaces import ISAPLMenuItem
from interlegis.portalmodelo.pl.setuphandlers import create_legislature_structure
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api

import unittest


class LegislatureStructureTestCase(unittest.TestCase):
    """Ensure legislature structure is created and configured.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.id = 'processo-legislativo'
        self.root = self.portal[self.id]

    def test_root_folder(self):
        self.assertEqual(api.content.get_state(self.root), 'published')
        self.assertIn('parlamentares', self.root)
        self.assertIn('legislaturas', self.root)
        self.assertIn('mesa-diretora', self.root)

    def test_parliamentarians_folder(self):
        folder = self.root['parlamentares']
        types = ('Parliamentarian',)
        self.assertEqual(folder.getImmediatelyAddableTypes(), types)
        self.assertEqual(folder.getLocallyAllowedTypes(), types)
        self.assertEqual(api.content.get_state(folder), 'published')
        self.assertTrue(ISAPLMenuItem.providedBy(folder))
        self.assertEqual(folder.getLayout(), '@@parliamentarians')

    def test_legislature_folder(self):
        folder = self.root['legislaturas']
        types = ('Legislature',)
        self.assertEqual(folder.getImmediatelyAddableTypes(), types)
        self.assertEqual(folder.getLocallyAllowedTypes(), types)
        self.assertEqual(api.content.get_state(folder), 'published')

    def test_legislative_board_link(self):
        link = self.root['mesa-diretora']
        self.assertEqual(link.remoteUrl, '../processo-legislativo/@@mesa-diretora')
        self.assertEqual(api.content.get_state(link), 'published')

    def test_marker_interface_is_removed_at_uninstall(self):
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])
        folder = self.root['parlamentares']
        self.assertFalse(ISAPLMenuItem.providedBy(folder))
        self.assertEqual(folder.getLayout(), 'folder_listing')

    def test_structure_with_existing_folder(self):
        with api.env.adopt_roles(['Manager']):
            api.content.delete(self.root)
            obj = api.content.create(self.portal, type='Folder', id=self.id)
            create_legislature_structure(self.portal)

        self.assertEqual(api.content.get_state(obj), 'published')
        self.assertIn('parlamentares', obj)
        self.assertIn('legislaturas', obj)
        self.assertIn('mesa-diretora', obj)

    def test_structure_with_existing_object(self):
        with api.env.adopt_roles(['Manager']):
            api.content.delete(self.root)
            api.content.create(self.portal, type='Document', id=self.id)

        with self.assertRaises(RuntimeError):
            create_legislature_structure(self.portal)
