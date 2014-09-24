#coding:utf-8
'''
Created on 07.12.2010

@author: akvarats
'''

from django.test import TestCase

from m3.helpers.urls import get_action, get_pack, get_url, get_pack_url

import actions as test_actions

class ActionNamesTests(TestCase):
    
    def test_main(self):
        
        # проверяем все варианты экшенов для урлов
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction11'), '/urls-tests/pack1/action1')
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction12'), '/urls-tests/pack1/action2')
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction13'), '/urls-tests/pack1/action3')
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction21'), '/urls-tests/pack2/action1')
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction22'), '/urls-tests/pack2/action2')
        self.failUnlessEqual(get_url('tests.helpers.urls_tests.actions.TestAction23'), '/urls-tests/pack2/action3')
        
        # проверяем как прогружается объект экшена
        self.failUnlessEqual(get_action('tests.helpers.urls_tests.actions.TestAction21'), 
                             test_actions.TestAction21)
        
        # проверяем как прогружается объект пака
        self.failUnlessEqual(get_pack('tests.helpers.urls_tests.actions.TestActionPack2'), 
                             test_actions.TestActionPack2)
        
        # проверяем короткие имена
        self.failUnlessEqual(get_url('test-action-11'), '/urls-tests/pack1/action1')
        self.failUnlessEqual(get_url('test-action-12'), '/urls-tests/pack1/action2')
        self.failUnlessEqual(get_url('test-action-21'), '/urls-tests/pack2/action1')
        self.failUnlessEqual(get_url('test-action-22'), '/urls-tests/pack2/action2')
        
        # проверяем получение url набора экшенов
        self.failUnlessEqual(get_pack_url('tests.helpers.urls_tests.actions.TestActionPack1'), '/urls-tests/pack1')
        self.failUnlessEqual(get_pack_url('tests.helpers.urls_tests.actions.TestActionPack2'), '/urls-tests/pack2')
        # проверяем получение url набора экшенов по короткому имени
        self.failUnlessEqual(get_pack_url('test-action-12'), '/urls-tests/pack2')