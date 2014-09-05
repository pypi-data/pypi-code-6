"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
try:
    from cStringIO import StringIO
except:
    from io import BytesIO as StringIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client

from huron.blog.models import Post, Category
from huron.blog.feeds import LatestEntriesFeed
from huron.blog.sitemaps import BlogSitemap


class SimpleTest(TestCase):
    def test_get_published(self):
        """
        Tests that we have only 2 articles published
        """
        nb_posts = Post.objects.get_published().count()
        self.assertEqual(nb_posts, 2)

    def test_listing_views(self):
        c = Client()
        response = c.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_category_views(self):
        c = Client()
        response = c.get('/blog/default/')
        self.assertEqual(response.status_code, 200)

    def test_listing_empty_redirect(self):
        c = Client()
        response = c.get('/blog/page/2/')
        self.assertEqual(response.status_code, 302)

    def test_category_empty_redirect(self):
        c = Client()
        response = c.get('/blog/default/page/2/')
        self.assertEqual(response.status_code, 302)

    def test_single_views(self):
        c = Client()
        response = c.get('/blog/25/8/2014/why-php-development-sucks/')
        self.assertEqual(response.status_code, 200)

    def test_single_redirect(self):
        c = Client()
        response = c.get('/blog/14/7/2012/why-php-development-sucks/')
        self.assertEqual(response.status_code, 302)

    def test_single_unpublished(self):
        c = Client()
        response = c.get('/blog/25/8/2014/never-published-article/')
        self.assertEqual(response.status_code, 404)

    def test_category_title(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(str(category), 'Default')

    def test_post_title(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(str(post), 'My First article')

    def test_feed(self):
        latest_entries = LatestEntriesFeed()
        description = (u'<p>If we look at the PHP documentation, we can see '
                       'some mistakes.&nbsp;</p>\r\n\r\n<p>PHP developers '
                       'thinks they are great but they never try something '
                       'else than PHP.</p>\r\n')
        self.assertEqual(len(latest_entries.items()), 2)
        self.assertEqual(latest_entries.item_title(latest_entries.items()[0]),
                         'Why PHP development sucks')
        item_desc = latest_entries.item_description(latest_entries.items()[0])
        self.assertEqual(item_desc, description)

    def test_sitemap(self):
        sitemap = BlogSitemap()
        self.assertEqual(len(sitemap.items()), 2)
        self.assertEqual(sitemap.lastmod(sitemap.items()[0]).isoformat(),
                         '2014-08-25T08:42:13.918000+00:00')

    def test_new_entry(self):
        category = Category.objects.get(pk=1)
        post = Post.objects.create(title="New",
                                   article="test",
                                   slug="new",
                                   )
        self.assertIsNot(post.pk, None)
