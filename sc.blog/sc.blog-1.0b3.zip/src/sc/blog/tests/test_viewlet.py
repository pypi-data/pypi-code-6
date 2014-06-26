# -*- coding: utf-8 -*-

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView as View
from sc.blog.interfaces import IBlogLayer
from sc.blog.testing import INTEGRATION_TESTING
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletTestCase(unittest.TestCase):
    """for more information on how to test viewlets, see:
    http://developer.plone.org/views/viewlets.html#finding-viewlets-programmatically
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBlogLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def _get_viewlet_manager(self, context, request=None):
        if request is None:
            request = self.request
        view = View(context, request)
        manager = queryMultiAdapter(
            (context, request, view), IViewletManager, 'plone.abovecontent')

        return manager

    def test_viewlet_is_registered(self):
        context = self.portal
        manager = self._get_viewlet_manager(context)
        self.assertTrue(manager)

        manager.update()
        self.assertIn('sc.blog.blogheader', manager)

    def test_viewlet_order(self):
        context = self.portal
        manager = self._get_viewlet_manager(context)

        manager.update()
        self.assertEqual(len(manager.viewlets), 2)
        viewlets = [v.__name__ for v in manager.viewlets]
        self.assertListEqual(viewlets,
                             [u'plone.path_bar', u'sc.blog.blogheader'])

    def test_viewlet_is_available_on_blogs(self):
        self.folder.invokeFactory('Blog', 'blog')
        context = self.folder['blog']
        manager = self._get_viewlet_manager(context)

        manager.update()
        viewlet = manager['sc.blog.blogheader']
        viewlet.update()
        self.assertTrue(viewlet.available())

    def test_viewlet_is_available_on_posts(self):
        # a post, is almost everything inside a Blog
        self.folder.invokeFactory('Blog', 'blog')
        self.blog = self.folder['blog']
        self.blog.invokeFactory('News Item', 'post')
        context = self.blog['post']
        manager = self._get_viewlet_manager(context)

        manager.update()
        viewlet = manager['sc.blog.blogheader']
        viewlet.update()
        self.assertTrue(viewlet.available())

    def test_blog_url(self):
        self.folder.invokeFactory('Blog', 'blog')
        blog_url = 'http://nohost/plone/test-folder/blog'

        # first test in the context of a blog
        context = self.folder['blog']
        manager = self._get_viewlet_manager(context)

        manager.update()
        viewlet = manager['sc.blog.blogheader']
        viewlet.update()
        self.assertEqual(viewlet.blog_url(), blog_url)

        # now test in the context of a post
        self.folder.blog.invokeFactory('News Item', 'post')
        context = self.folder.blog['post']
        manager = self._get_viewlet_manager(context)

        manager.update()
        viewlet = manager['sc.blog.blogheader']
        viewlet.update()
        self.assertEqual(viewlet.blog_url(), blog_url)
