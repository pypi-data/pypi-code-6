# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.interfaces import IParliamentarian
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(self.portal, 'Folder', 'test-folder')

        self.parliamentarian = api.content.create(folder, 'Parliamentarian', 'parliamentarian')

    def test_adding(self):
        self.assertTrue(IParliamentarian.providedBy(self.parliamentarian))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Parliamentarian')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Parliamentarian')
        schema = fti.lookupSchema()
        self.assertEqual(IParliamentarian, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Parliamentarian')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IParliamentarian.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.parliamentarian))
        self.assertTrue(IAttributeUUID.providedBy(self.parliamentarian))

    def test_discussion_is_disabled(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        self.assertFalse(fti.allow_discussion)
