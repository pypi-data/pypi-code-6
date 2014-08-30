# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.interfaces import ILegislature
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
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

        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(self.portal, 'Folder', 'test-folder')

        self.legislature = api.content.create(folder, 'Legislature', 'legislature')

    def test_adding(self):
        self.assertTrue(ILegislature.providedBy(self.legislature))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Legislature')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Legislature')
        schema = fti.lookupSchema()
        self.assertEqual(ILegislature, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Legislature')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ILegislature.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.legislature))
        self.assertTrue(IAttributeUUID.providedBy(self.legislature))

    def test_allowed_content_types(self):
        expected = ['Session']
        allowed_types = [t.getId() for t in self.legislature.allowedContentTypes()]
        self.assertListEqual(expected, allowed_types)

        # trying to add any other content type raises an error
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.legislature, 'Document', 'foo')

    def test_discussion_is_disabled(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        self.assertFalse(fti.allow_discussion)
