# coding: utf-8
"""
File: test_manage_command.py
Author: Rinat F Sabitov
Description:
"""


import os
import tempfile
from unittest import TestCase
import django.conf

from .env import LICENSE, PUBLIC_KEY, INVALID_SIGNATURE_LICENSE


class LicenseMiddlewareTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
            )

    def test_valid_license(self):
        from django.core.management import call_command
        tmp_file, tmp_filename = tempfile.mkstemp()
        with os.fdopen(tmp_file, 'w') as f:
            f.write(LICENSE)
        django.conf.settings.LIC_KEY_FILE = tmp_filename
        django.conf.settings.PUBLIC_KEY = PUBLIC_KEY
        django.conf.settings.INSTALLED_APPS = ['m3_license', ]

        with self.assertRaises(SystemExit) as cm:
            call_command('license_status')

        self.assertEqual(cm.exception.code, 0)

    def test_invalid_license(self):
        from django.core.management import call_command
        tmp_file, tmp_filename = tempfile.mkstemp()
        with os.fdopen(tmp_file, 'w') as f:
            f.write(INVALID_SIGNATURE_LICENSE)
        django.conf.settings.LIC_KEY_FILE = tmp_filename
        django.conf.settings.PUBLIC_KEY = PUBLIC_KEY
        django.conf.settings.INSTALLED_APPS = ['m3_license', ]

        with self.assertRaises(SystemExit) as cm:
            call_command('license_status')

        self.assertEqual(cm.exception.code, 1)
