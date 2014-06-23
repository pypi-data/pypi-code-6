from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabeling
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestTestingBuidlers(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_label_root_builder(self):
        root = create(Builder('label root')
                      .with_labels(('Questions', 'blue'),
                                   ('Bugs', 'red')))

        self.assertItemsEqual(
            [{'label_id': 'questions',
              'title': 'Questions',
              'color': 'blue'},
             {'label_id': 'bugs',
              'title': 'Bugs',
              'color': 'red'}],
            ILabelJar(root).list())

    def test_labelled_page_builder(self):
        root = create(Builder('label root')
                      .with_labels(('Questions', 'blue'),
                                   ('Bugs', 'red'),
                                   ('Enhancements', 'green')))

        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('questions', 'bugs'))

        self.assertItemsEqual(
            [{'label_id': 'questions',
              'title': 'Questions',
              'color': 'blue'},
             {'label_id': 'bugs',
              'title': 'Bugs',
              'color': 'red'}],
            ILabeling(page).active_labels())
