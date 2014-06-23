from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.interfaces import ILabeling
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase
from zExceptions import Unauthorized


class TestLabelingView(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    @browsing
    def test_activate_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red'),
                                   ('Feature', 'blue')))
        page = create(Builder('labelled page').within(root))
        self.assertFalse(self.indexed_labels_for(page))

        browser.login().open(page,
                             view='labeling/update',
                             data={'activate_labels': ['question', 'bug']})

        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple'},
             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabeling(page).active_labels())

        self.assertItemsEqual(['question', 'bug'], self.indexed_labels_for(page))

    @browsing
    def test_deactivate_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red'),
                                   ('Feature', 'blue')))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bug'))

        browser.login().open(page,
                             view='labeling/update',
                             data={})

        self.assertItemsEqual(
            [],
            ILabeling(page).active_labels())

    @browsing
    def test_mixed_updating_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red'),
                                   ('Feature', 'blue')))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bug'))

        browser.login().open(page,
                             view='labeling/update',
                             data={'activate_labels': ['question','feature']})


        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple'},
             {'label_id': 'feature',
              'title': 'Feature',
              'color': 'blue'}],
            ILabeling(page).active_labels())

    @browsing
    def test_updating_is_protected(self, browser):
        root = create(Builder('label root'))
        page = create(Builder('labelled page').within(root))
        browser.login(create(Builder('user').with_roles('Reader')))

        with self.assertRaises(Unauthorized):
            browser.open(page,
                         view='labeling/update',
                         data={'question': 'yes',
                               'feature': 'yes'})

    def indexed_labels_for(self, obj):
        catalog = getToolByName(self.portal, 'portal_catalog')
        rid = catalog.getrid('/'.join(obj.getPhysicalPath()))
        return catalog.getIndexDataForRID(rid).get('labels')
