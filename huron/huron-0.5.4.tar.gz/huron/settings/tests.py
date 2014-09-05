# -*- coding: utf-8 -*-
from django.test import TestCase

from huron.settings.models import Setting
from huron.settings.context_processors import get_settings
from huron.settings.templatetags.settings_custom import get_value

class SettingTestCase(TestCase):

    def setUp(self):
        Setting.objects.create(key=u"is_active", value=False)
        Setting.objects.create(key=u"by_pages", value=100)

    def test_basic_usage(self):
        fake_request = None
        ctx = get_settings(fake_request)
        self.assertEqual(get_value(ctx['settings'], 'is_active'), 'False')

    def test_str_settings(self):
        setting = Setting.objects.get(pk=1)
        self.assertEqual(str(setting), 'is_active')
