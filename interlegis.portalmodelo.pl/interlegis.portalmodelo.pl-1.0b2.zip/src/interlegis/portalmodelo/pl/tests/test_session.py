# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.interfaces import ISession
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
            folder = api.content.create(self.portal, 'Legislature', 'legislature')

        self.session = api.content.create(folder, 'Session', 'session')

    def test_adding(self):
        self.assertTrue(ISession.providedBy(self.session))

    def test_adding_outside_container(self):
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.portal, 'Session', 'foo')

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        schema = fti.lookupSchema()
        self.assertEqual(ISession, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISession.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.session))
        self.assertTrue(IAttributeUUID.providedBy(self.session))

    def test_discussion_is_disabled(self):
        fti = queryUtility(IDexterityFTI, name='Session')
        self.assertFalse(fti.allow_discussion)
