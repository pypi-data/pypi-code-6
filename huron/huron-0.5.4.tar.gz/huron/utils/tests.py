# -*- coding: utf-8 -*-
"""
    Test utils
"""
from django.test import TestCase

from huron import get_version


class HuronTestCase(TestCase):

    def setUp(self):
        self.version = get_version()

    def test_version(self):
        self.assertEqual(self.version, '0.5.4')
