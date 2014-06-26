# -*- coding: utf-8 -*-
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from sc.blog.content import IBlog
from sc.blog.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                self.portal, 'Folder', 'test-folder')

        self.blog = api.content.create(self.folder, 'Blog', 'blog')

    def test_adding(self):
        self.assertTrue(IBlog.providedBy(self.blog))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Blog')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Blog')
        schema = fti.lookupSchema()
        self.assertEqual(IBlog, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Blog')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IBlog.providedBy(new_object))

    def test_can_be_excluded_from_navigation(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.blog))
        self.assertTrue(hasattr(self.blog, 'exclude_from_nav'))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.blog))
        self.assertTrue(IAttributeUUID.providedBy(self.blog))

    def test_supports_object_relations(self):
        from plone.app.relationfield.behavior import IRelatedItems
        self.assertTrue(IRelatedItems.providedBy(self.blog))

    def test_blogs_can_not_contain_blogs(self):
        from plone.app.content.browser.folderfactories import _allowedTypes
        request = self.layer['request']

        def allowed_types(container):
            return [i.id for i in _allowedTypes(request, container)]

        # Blogs can't contain Blogs
        self.assertIn('Blog', allowed_types(self.folder))
        self.assertNotIn('Blog', allowed_types(self.blog))
        # not allowed in subobjects too
        api.content.create(self.blog, 'Folder', 'subfolder')
        self.assertNotIn('Blog', allowed_types(self.blog['subfolder']))
