import os

from django.test import TestCase, Client
from django.contrib import admin

from jmb.core import conf

admin.autodiscover()

class FirstTest(TestCase):

    # def setUp(self):
    #     self.client.login(username='admin', password='')

    def test_00(self):
        "Prova di test"
        self.assert_(True)
