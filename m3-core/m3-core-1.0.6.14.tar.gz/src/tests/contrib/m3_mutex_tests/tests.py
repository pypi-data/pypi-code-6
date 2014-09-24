#coding:utf-8
'''
Created on 22.07.2011

@author: akvarats
'''

import time

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from m3.core.middleware import ThreadData
from m3.helpers import urls

from m3_mutex.helpers import get_default_owner


class InfrastractureTests(TestCase):
    '''
    Тесты на выполнение инфраструктурных операций
    '''
    
    def test_default_owner(self):
        '''
        Проверяем как по умолчанию определяются параметры владельца семафора. 
        '''
        default_owner = get_default_owner()
        
        self.assertEqual(default_owner.session_id, ThreadData.DEFAULT_SESSION_KEY)
        self.assertEqual(default_owner.host, ThreadData.DEFAULT_CLIENT_HOST)
        self.assertEqual(default_owner.user_id, ThreadData.DEFAULT_USER_ID)
        self.assertEqual(default_owner.name, ThreadData.DEFAULT_USER_NAME)
        self.assertEqual(default_owner.login, ThreadData.DEFAULT_USER_LOGIN)
        

class MutexTests(TestCase):
    '''
    Тесты на выполнение основных операций с семафорами
    '''
    
    def setUp(self):
        admin = User()
        admin.username = 'admin'
        admin.set_password('admin')
        admin.save()
        
        user = User()
        user.username = 'user'
        user.set_password('user')
        user.save()
    
        
        
    def test1_capture(self):
        '''
        Сценарий:
        1. захватываем семафор клиентом 1
        2. проверяем владельца семафора клиентом 1
        3. проверяем владельца семафора клиентом 2
        4. пытаемся захватить семафор клиентом 2
        5. пытаемся освободить семафор клиентом 2
        6. освобождаем семафор клиентом 1
        7. захватываем семафор клиентом 2
        8. проверяем владельца семафора клиентом 2
        9. проверяем владельца семафора клиентом 1
        10. освобождаем семафор клиентом 2
        11. проверяем семафор клиентом 3
        '''
        mutex_id_params = {'mutex_group': 'group1',
                           'mutex_mode': 'mode1',
                           'mutex_id': 'id1'}
        
        client1 = Client()
        client1.login(username='admin', password='admin')
        
        client2 = Client()
        client2.login(username='user', password='user')
        
        client3 = Client()
        
        # 1. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 2. проверяем владельца семафора клиентом 1
        response = client1.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'CAPTURED_BY_ME')
        
        # 3. проверяем владельца семафора клиентом 2
        response = client2.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'CAPTURED_BY_OTHER')
        
        # 4. пытаемся захватить семафор клиентом 2
        response = client2.post(urls.get_url('mutex.capture-fail'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 5. пытаемся освободить семафор клиентом 2
        response = client2.post(urls.get_url('mutex.release-fail'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 6. освобождаем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.release-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 7. захватываем семафор клиентом 2
        response = client2.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 8. проверяем владельца семафора клиентом 1
        response = client2.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'CAPTURED_BY_ME')
        
        # 9. проверяем владельца семафора клиентом 2
        response = client1.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'CAPTURED_BY_OTHER')
        
        # 10. освобождаем семафор клиентом 2
        response = client2.post(urls.get_url('mutex.release-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 11. проверяем семафор клиентом 3
        response = client3.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'FREE')
        
    def test2_autorelease(self):
        '''
        Тест на автоосвобождение семафора
        
        # 1. захватываем семафор клиентом 1 с таймаутом в 2 секунды
        # 2. проверяем семафор клиентом 2
        # 3. ждем 3 секунд
        # 4. проверяем семафор клиентом 2
        # -----------------
        # 5. захватываем семафор клиентом 2 с таймаутом в 2 секунды
        # 6. захватываем семафор клиентом 1
        # 7. ждем 3 секунд
        # 8. захватываем семафор клиентом 1
        # 9. освобождаем семафор клиентом 1
        '''
        mutex_id_params = {'mutex_group': 'group2',
                           'mutex_mode': 'mode2',
                           'mutex_id': 'id2'}
        
        client1 = Client()
        client1.login(username='admin', password='admin')
        
        client2 = Client()
        client2.login(username='admin', password='admin')
        
        # 1. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-short'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 2. проверяем владельца семафора клиентом 2
        response = client2.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'CAPTURED_BY_OTHER')
        
        # 3. ждем 3 секунд
        time.sleep(3)
        
        # 4. проверяем семафор клиентом 2
        response = client2.post(urls.get_url('mutex.request'), mutex_id_params)
        self.assertEqual(response.content, 'FREE')
        
        # -----------------
        # 5. захватываем семафор клиентом 2 с таймаутом в 2 секунды
        response = client2.post(urls.get_url('mutex.capture-short'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 6. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-fail'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 7. ждем 3 секунд
        time.sleep(3)
        
        # 8. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 9. освобождаем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.release-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
    def test3_status_data(self):
        '''
        Тест на сохранение и чтение статусной информации
        '''
        status_data = u'1234567890'
        
        mutex_id_params = {'mutex_group': 'group2',
                           'mutex_mode': 'mode2',
                           'mutex_id': 'id2',
                           'status_data': status_data,}
        
        client1 = Client()
        client1.login(username='admin', password='admin')
        
        # 1. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 2. проверяем владельца семафора клиентом 1
        response = client1.post(urls.get_url('mutex.status-data'), mutex_id_params)
        self.assertEqual(response.content, status_data)
        
        # 3. освобождаем семафор
        response = client1.post(urls.get_url('mutex.release-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
    def test4_refresh_mutex(self):
        '''
        Тесты на корректное обновление мютекса
        '''
        status_data = u'1234567890'
        new_status_data = u'0987654321'
        
        mutex_id_params = {'mutex_group': 'group2',
                           'mutex_mode': 'mode2',
                           'mutex_id': 'id2',
                           'status_data': status_data,}
        
        client1 = Client()
        client1.login(username='admin', password='admin')
        
        # 1. захватываем семафор клиентом 1
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        time.sleep(1)
        
        # 2. должен сработать refresh
        mutex_id_params['status_data'] = ''
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 3. запрашиваем данные семафора (должны прийти старые данные)
        response = client1.post(urls.get_url('mutex.status-data'), mutex_id_params)
        self.assertEqual(response.content, status_data)
        
        # 4. отправляем новые статусные данные
        mutex_id_params['status_data'] = new_status_data
        response = client1.post(urls.get_url('mutex.capture-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')
        
        # 5. проверяем новые статусные данные
        response = client1.post(urls.get_url('mutex.status-data'), mutex_id_params)
        self.assertEqual(response.content, new_status_data)
        
        # 6. освобождаем семафор
        response = client1.post(urls.get_url('mutex.release-ok'), mutex_id_params)
        self.assertEqual(response.content, 'ok')