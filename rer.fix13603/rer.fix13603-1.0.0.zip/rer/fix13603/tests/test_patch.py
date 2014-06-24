# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName
from rer.fix13603.testing import RERFIXDELETE_FUNCTIONAL_TESTING
import unittest


class TestDeletePatch(unittest.TestCase):

    layer = RERFIXDELETE_FUNCTIONAL_TESTING

    def setUp(self):
        """
        """
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, TEST_USER_NAME)
        #create the structure
        self.portal.invokeFactory('Folder', 'foo')
        self.portal.invokeFactory('Folder', 'bar')
        bar = self.portal['bar']
        bar.invokeFactory('Folder', 'bar-sub')
        bar_sub = bar['bar-sub']
        bar_sub.invokeFactory('Document', 'foo')

    def test_delete_objects_by_path(self):
        putils = getToolByName(self.portal, 'plone_utils')
        paths = ['/plone/bar/bar-sub/foo']
        success1, failure1 = putils.deleteObjectsByPaths(paths, REQUEST={'method': 'POST'})
        success2, failure2 = putils.deleteObjectsByPaths(paths, REQUEST={'method': 'POST'})
        self.assertEqual(success1, ['foo (/plone/bar/bar-sub/foo)'])
        self.assertEqual(success2, [])
        self.assertEqual(failure1, {})
        self.assertNotEqual(failure2, {})
        self.assertTrue(self.portal.get('foo', None))
