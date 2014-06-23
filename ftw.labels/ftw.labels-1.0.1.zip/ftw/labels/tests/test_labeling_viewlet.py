from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestLabelingViewlet(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.root = create(Builder('label root')
                           .with_labels(('Label 1', ''), ('Label 2', '')))
        self.document = create(Builder('labelled page').within(self.root))

    @browsing
    def test_no_labeling_viewlet_if_no_available_labels(self, browser):
        no_label_root = create(Builder('label root'))
        no_label_document = create(Builder('labelled page').within(no_label_root))
        browser.open(no_label_document)
        self.assertFalse(browser.css('#labeling-viewlet'))

    @browsing
    def test_show_labeling_viewlet_if_available_labels(self, browser):
        browser.open(self.document)
        self.assertTrue(browser.css('#labeling-viewlet'))

    @browsing
    def test_users_with_permission_can_view_manage_link(self, browser):
        editor = create(Builder('user').with_roles('Editor'))
        browser.login(editor).open(self.document)
        self.assertTrue(browser.css('#labeling-viewlet #toggle-label-form'))

    @browsing
    def test_users_without_permission_cant_view_manage_link(self, browser):
        reader = create(Builder('user').with_roles('Reader'))
        browser.login(reader).open(self.document)
        self.assertFalse(browser.css('#labeling-viewlet #toggle-label-form'))
