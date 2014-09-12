from itertools import groupby
import random

from django import forms
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase, override_settings
from lxml import html

from setmagic.models import Setting
from setmagic.wrapper import SettingsWrapper


test_schema = [
    ('Test group 1', [
        dict(
            name='SETTING1',
            label='Setting 1',
            help_text='Help text for setting 1',
            default='Default value'),
        dict(
            name='SETTING2',
            label='Setting 2',
            help_text='Help text for setting 2'),
    ]),
    ('Test group 2', [
        dict(
            name='SETTING3',
            label='Setting 3',
            help_text='Help text for setting 3'),
        dict(
            name='SETTING4',
            label='Setting 4',
            help_text='Help text for setting 4'),
        dict(
            name='SETTING5',
            label='Setting 5',
            help_text='Help text for setting 5'),
    ]),
    ('Typed settings group', [
        dict(
            name='EMAIL',
            label='Test email',
            help_text='Some text email',
            field=forms.EmailField()),
    ]),
]


class SetMagicTestCase(TransactionTestCase):

    def setUp(self):
        self.setmagic = SettingsWrapper()
        self.setmagic._sync()


@override_settings(SETMAGIC_SCHEMA=test_schema)
class GetSetSettingsTestCase(SetMagicTestCase):

    def test_set_setting(self):
        new_value = 'value1'
        self.setmagic.SETTING1 = new_value

        # Check from the settings wrapper
        self.assertEqual(self.setmagic.SETTING1, new_value)

        # Check directly from database
        self.assertTrue(Setting.objects.exists())
        db_object = Setting.objects.get(name='SETTING1')
        self.assertEqual(db_object.current_value, new_value)
        self.assertEqual(db_object.current_value, new_value)

    def test_setting_default_value(self):
        # The default value is pre-set at the setting
        self.assertEqual(
            self.setmagic.SETTING1,
            self.setmagic.defs['SETTING1']['default'])


@override_settings(SETMAGIC_SCHEMA=[])
class SettingsAdminTestCase(SetMagicTestCase):

    fixtures = ['setmagic_test_users']
    reset_sequences = True

    def setUp(self):
        super(SettingsAdminTestCase, self).setUp()
        self.client.login(username='root', password='123')

    def test_changelist_order(self):
        url = reverse('admin:setmagic_setting_changelist')

        # Check a randomized settings order
        new_schema = test_schema[:]
        random.shuffle(new_schema)

        with self.settings(SETMAGIC_SCHEMA=new_schema):
            self.setUp()

            dom = html.fromstring(self.client.get(url).content)

            expected = [
                (group_label, [d['name'] for d in defs],)
                for group_label, defs in groupby(
                    self.setmagic.defs.values(), lambda d: d['group_label'])]

            rendered = [
                (
                    section.xpath('h2/text()')[0],
                    section.xpath('*//*[@data-setting-name]/text()'),
                )
                for section in dom.xpath('//*[@data-settings-formset]')]

            self.assertEqual(expected, rendered)

    @override_settings(SETMAGIC_SCHEMA=test_schema)
    def test_changelist_custom_field(self):
        url = reverse('admin:setmagic_setting_changelist')
        dom = html.fromstring(self.client.get(url).content)
        self.assertTrue(dom.xpath('//input[@type="email"]'))
