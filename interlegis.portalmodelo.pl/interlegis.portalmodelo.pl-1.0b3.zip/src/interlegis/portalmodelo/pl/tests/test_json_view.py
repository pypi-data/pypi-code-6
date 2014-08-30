# -*- coding: utf-8 -*-
from interlegis.portalmodelo.pl.sync.controlpanel import ISyncSettings
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import os
import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.maxDiff = None
        self.view = api.content.get_view(
            name='pl-json', context=self.portal, request=self.request)
        with api.env.adopt_roles(['Manager']):
            self.load_data()

    def load_data(self):
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISyncSettings)
        path = os.path.join(os.path.dirname(__file__))
        self.remote = 'file://' + os.path.join(path, 'sapl.json')
        self.settings.path = u'/processo-legislativo'
        self.settings.remote = unicode(self.remote)
        self.folder = self.portal['processo-legislativo']
        view = api.content.get_view(
            name='sync-sapl', context=self.portal, request=self.request)
        view()

    def test_get_legislatures(self):
        self.view.update()
        results = self.view.get_legislatures()
        self.assertEqual(len(results), 1)
        self.assertEqual(type(results[0]), dict)
        self.assertDictEqual(
            results[0],
            {
                'description': u'',
                'end_date': '2016-12-31',
                'members': [
                    '/plone/processo-legislativo/parlamentares/000000000001',
                    '/plone/processo-legislativo/parlamentares/000000000002',
                ],
                'start_date': '2013-01-01',
                'title': u'1st Legislature',
                'uri': 'http://nohost/plone/processo-legislativo/legislaturas/legislature-01',
            }
        )

    def test_get_parliamentarians(self):
        self.view.update()
        results = self.view.get_parliamentarians()
        self.assertEqual(len(results), 2)
        self.assertEqual(type(results[0]), dict)
        self.assertDictEqual(
            results[0],
            {
                'address': u'Av. N2, Anexo E do Senado Federal, Brasilia/DF',
                'birthday': '1943-01-09',
                'description': u'Bruxo do Cosme Velho, escritor.',
                'email': u'',
                'full_name': u'Joaquim Maria Machado de Assis',
                'image': '',
                'party_affiliation': [{
                    'date_affiliation': '1975-12-19',
                    'date_disaffiliation': '',
                    'party': u'ABL',
                }],
                'postal_code': u'70165-900',
                'site': u'',
                'telephone': u'+55615553213',
                'title': u'Machado de Assis',
                'uri': 'http://nohost/plone/processo-legislativo/parlamentares/000000000001',
            }
        )
