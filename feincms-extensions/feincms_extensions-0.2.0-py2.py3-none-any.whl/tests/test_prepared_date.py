from unittest.mock import patch

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from .factories import PageFactory


class TestExtension(TestCase):
    def test_prepared_date_empty(self):
        page = PageFactory.create()

        self.assertEqual(page.prepared_date, '')

    def test_set_prepared_date(self):
        prepared_date = 'Sample data'
        page = PageFactory.create()
        page.prepared_date = prepared_date
        self.assertEqual(page.prepared_date, prepared_date)

    def test_prepared_date_parent(self):
        prepared_date = 'Sample data'
        parent = PageFactory.create(prepared_date=prepared_date, slug='a')
        page = PageFactory.create(parent=parent, slug='b')

        self.assertEqual(page.prepared_date, prepared_date)

    def test_prepared_date_override_url(self):
        prepared_date = 'Sample data'
        PageFactory.create(prepared_date=prepared_date, override_url='/')
        page = PageFactory.create(slug='page')

        self.assertEqual(page.prepared_date, prepared_date)

    @patch('feincms.module.page.modeladmins.PageAdmin.add_extension_options')
    def test_handle_modeladmin(self, add_extension_options):
        # Force admin extension mechanism to be called
        from feincms.module.page.admin import PageAdmin
        add_extension_options.assert_called_once_with(_('Date of Preparation'), {
            'fields': ('_prepared_date',),
            'classes': ('collapse',),
        })
