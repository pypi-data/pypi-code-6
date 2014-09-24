# coding: utf-8
"""
File: test_middleware.py
Author: Rinat F Sabitov
Description:
"""

import os
import tempfile
import datetime
from mock import Mock
from m3_license.middleware import LicenseMiddleware
from m3_license.api import LicenseException

from unittest import TestCase
import django.conf

from .env import LICENSE, PUBLIC_KEY


class LicenseMiddlewareTest(TestCase):

    def setUp(self):
        self.lm = LicenseMiddleware()
        self.request = Mock()
        tmp_file, self.tmp_filename = tempfile.mkstemp()
        with os.fdopen(tmp_file, 'w') as f:
            f.write(LICENSE)
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
            )

    def test_process_request(self):
        django.conf.settings.LIC_KEY_FILE = self.tmp_filename
        django.conf.settings.PUBLIC_KEY = PUBLIC_KEY
        self.lm.process_request(self.request)
        self.assertEqual(self.request.license['organization'],
            u'Ключ для Некоммерческого использования Ветеринария')

        self.assertIsInstance(self.request.license['startdate'], datetime.date)
        self.assertIsInstance(self.request.license['enddate'], datetime.date)

    def test_exceptions(self):
        del django.conf.settings.LIC_KEY_FILE
        del django.conf.settings.PUBLIC_KEY

        self.assertRaises(LicenseException,
            self.lm.process_request, self.request)
        django.conf.settings.LIC_KEY_FILE = self.tmp_filename
        self.assertRaises(LicenseException,
            self.lm.process_request, self.request)
        del django.conf.settings.LIC_KEY_FILE
        django.conf.settings.PUBLIC_KEY = PUBLIC_KEY
        self.assertRaises(LicenseException,
            self.lm.process_request, self.request)
