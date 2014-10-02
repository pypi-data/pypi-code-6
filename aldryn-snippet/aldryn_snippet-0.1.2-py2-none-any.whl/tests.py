# -*- coding: utf-8 -*-
import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cms import api
from cms.models import CMSPlugin
from cms.test_utils.testcases import BaseCMSTestCase, URL_CMS_PLUGIN_ADD, URL_CMS_PLUGIN_EDIT
from cms.utils import get_cms_setting

from .cms_plugins import Snippet


class SnippetTestCase(TestCase, BaseCMSTestCase):
    su_username = 'user'
    su_password = 'pass'
    random = []

    def get_random_string(self, length=20):
        """
        Returns a random string with length ``length`` which has not been used in this class before
        """
        rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        if rand in self.random:
            rand = self.get_random_string(length)  # pragma: no cover
        self.random.append(rand)
        return rand

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page('page', self.template, self.language, published=True)
        self.placeholder = self.page.placeholders.all()[0]
        self.superuser = self.create_superuser()

    def create_superuser(self):
        return User.objects.create_superuser(self.su_username, 'email@example.com', self.su_password)

    def test_add_snippet_plugin_api(self):
        content = self.get_random_string()
        plugin = api.add_plugin(self.placeholder, Snippet, self.language)

        plugin.content = content
        plugin.save()
        self.page.publish(self.language)

        response = self.client.get(self.page.get_absolute_url())
        self.assertContains(response, content)

    def test_add_snippet_plugin_client(self):
        self.client.login(username=self.su_username, password=self.su_password)

        content = self.get_random_string()
        plugin_data = {
            'plugin_type': 'Snippet',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
            'content': content,
        }

        # Add plugin
        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CMSPlugin.objects.exists())

        # Edit plugin
        edit_url = '%s%d/' % (URL_CMS_PLUGIN_EDIT, CMSPlugin.objects.all()[0].pk)
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        data = {'content': content}
        response = self.client.post(edit_url, data)
        self.assertEqual(response.status_code, 200)

        # Check plugin content
        self.page.publish(self.language)
        self.client.logout()

        response = self.client.get(self.page.get_absolute_url())
        self.assertContains(response, content)
