# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase
from django.utils.datastructures import MultiValueDict
from django.utils.http import urlencode

from .models import ChickenWings


class ChickenWingsListViewTestCase(TestCase):

    def test_no_pizzas(self):
        p = ChickenWings.objects.all()
        self.assertEqual(len(p), 0, 'Test requires no wings')
        response = self.client.get(reverse('ftw:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No chicken wings found' in response.content.decode('utf-8'))

    def test_many_pizzas(self):
        NUM_WINGS = 30
        wings = []
        for n in range(NUM_WINGS):
            p = ChickenWings.objects.create(flavour=[ChickenWings.HONEY_BBQ])
            wings.append(p)

        self.assertEqual(len(wings), NUM_WINGS, 'Test requires chicken wings')
        response = self.client.get(reverse('ftw:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (ChickenWings.HONEY_BBQ) in response.content.decode('utf-8'))


class ChickenWingsCreateViewTestCase(TestCase):

    def test_view(self):
        response = self.client.get(reverse('ftw:create'))
        self.assertEqual(response.status_code, 200)

    def test_creation_single(self):
        data = {
            'flavour': [ChickenWings.JERK]
        }
        response = self.client.post(
            reverse('ftw:create'),
            urlencode(MultiValueDict(data), doseq=True),
            content_type='application/x-www-form-urlencoded'
            )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'http://testserver' + reverse('pizza:created'))
        p = ChickenWings.objects.all()[0]
        self.assertIn(ChickenWings.JERK, p.flavour)

    def test_creation_multiple(self):
        data = {
            'toppings': [ChickenWings.SUICIDE, ChickenWings.BOURBON]
        }
        response = self.client.post(
            reverse('ftw:create'),
            urlencode(MultiValueDict(data), doseq=True),
            content_type='application/x-www-form-urlencoded'
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'http://testserver' + reverse('ftw:created'))
        p = Pizza.objects.all()[0]
        self.assertIn(ChickenWings.SUICIDE, p.flavour)
        self.assertIn(ChickenWings.BOURBON, p.flavour)