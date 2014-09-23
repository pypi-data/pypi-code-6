#coding:utf-8
'''
Created on 18.11.11
@author: akvarats
'''

import uuid
import json
import time

from django.test import TestCase
from django.test.client import Client

from m3.helpers import urls

import urllib2

class AsyncTests(TestCase):

    def send_request(self, path='/', data=None):



    def test_mutex_async(self):

        boundary = str(uuid.uuid4())

        client = Client()

        resp = client.post(path=urls.get_url('actions-tests.alive'),
                           data={'print me': 'print-print-print me!!!',})

        self.assertEqual(resp.content, 'ok')

        # 1. проверяем состояние неначатой операции
        resp = client.post(path=urls.get_url('actions-tests.background'),
                           data={'command': 'request',
                                 'boundary': boundary})

        result = json.JSONDecoder().decode(resp.content)
        self.assertFalse(result['alive'])

        # 2. стартуем операцию
        resp = client.post(path=urls.get_url('actions-tests.background'),
                           data={'command': 'start',
                                 'boundary': boundary})

        result = json.JSONDecoder().decode(resp.content)
        self.assertTrue(result['alive'])

        while True:
            resp = client.post(path=urls.get_url('actions-tests.background'),
                   data={'command': 'request',
                         'boundary': boundary})
            result = json.JSONDecoder().decode(resp.content)
            if result['alive']:
                print u'Операция выполняется. Прогресс: %s' % result['value']
            else:
                print u'Операция завершена'
                break
            time.sleep(1)

