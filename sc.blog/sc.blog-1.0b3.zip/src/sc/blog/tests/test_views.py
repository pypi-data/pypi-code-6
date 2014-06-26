# -*- coding: utf-8 -*-

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from sc.blog.testing import FUNCTIONAL_TESTING

import transaction
import unittest


class ViewsTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Blog', 'b1')
        self.b1 = self.portal['b1']
        self.b1.invokeFactory('Document', 'doc1')
        self.b1.invokeFactory('News Item', 'news1')
        self.b1.invokeFactory('Folder', 'folder1')
        self.b1.folder1.invokeFactory('Document', 'doc1.1')
        transaction.commit()

    def test_default_view(self):
        browser = Browser(self.app)
        portal_url = self.portal.absolute_url()
        # Go admin
        browser.open(portal_url + "/login_form")
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

        browser.open('%s/b1' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertTrue('<a href="http://nohost/plone/b1/doc1" class="summary url"></a>' in browser.contents)
        self.assertTrue('<a href="http://nohost/plone/b1/news1" class="summary url"></a>' in browser.contents)
        self.assertFalse('<a href="http://nohost/plone/b1/folder1" class="summary url"></a>' in browser.contents)
        self.assertTrue('<a href="http://nohost/plone/b1/folder1/doc1.1" class="summary url"></a>' in browser.contents)

    def test_blog_summary_view(self):
        browser = Browser(self.app)
        portal_url = self.portal.absolute_url()
        # Go admin
        browser.open(portal_url + "/login_form")
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

        browser.open('%s/b1/blog_summary_view' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertTrue('<a href="http://nohost/plone/b1/doc1" class="summary url">doc1</a>' in browser.contents)
        self.assertTrue('<a href="http://nohost/plone/b1/news1" class="summary url">news1</a>' in browser.contents)
        self.assertFalse('<a href="http://nohost/plone/b1/folder1" class="summary url">folder1</a>' in browser.contents)
        self.assertTrue('<a href="http://nohost/plone/b1/folder1/doc1.1" class="summary url">doc1.1</a>' in browser.contents)
