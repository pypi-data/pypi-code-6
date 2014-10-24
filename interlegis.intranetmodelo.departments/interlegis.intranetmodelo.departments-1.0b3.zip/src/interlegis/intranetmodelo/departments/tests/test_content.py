# -*- coding: utf-8 -*-

from interlegis.intranetmodelo.departments.interfaces import IDepartment
from interlegis.intranetmodelo.departments.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Department', 'department')
        self.department = self.folder['department']

    def test_adding(self):
        self.assertTrue(IDepartment.providedBy(self.department))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Department')
        self.assertIsNotNone(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Department')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IDepartment.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.department))
        self.assertTrue(IAttributeUUID.providedBy(self.department))
