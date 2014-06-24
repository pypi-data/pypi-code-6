from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.interfaces import ILabeling
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestCatalogIndex(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_index_is_registered(self):
        self.assertIn('labels', self.catalog.indexes())

    def test_updating_index(self):
        root = create(Builder('label root')
                      .with_labels(('Question', 'blue'),
                                   ('Bugs', 'red'),
                                   ('Enhancements', 'green')))

        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bugs'))

        self.assertFalse(self.index_data_for(page).get('labels'))

        ILabeling(page).update(['bugs', 'question'])
        page.reindexObject(idxs=['labels'])

        self.assertItemsEqual(
            ['bugs', 'question'],
            self.index_data_for(page).get('labels'))

    def index_data_for(self, obj):
        rid = self.catalog.getrid('/'.join(obj.getPhysicalPath()))
        return self.catalog.getIndexDataForRID(rid)
