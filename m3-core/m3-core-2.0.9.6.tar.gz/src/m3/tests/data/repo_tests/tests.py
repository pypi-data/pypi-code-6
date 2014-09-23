#coding:utf-8
'''
Created on 27.07.2011

@author: akvarats
'''

from django.test import TestCase

from m3.data.proxy import Proxy

from domain import Contragent, LPU

class ProxyTests(TestCase):
    
    def setUp(self):
        pass
    
    def test_1(self):
        '''
        '''
        proxy = Proxy.create([Contragent, LPU])
        
        proxy.code = 'code'
        proxy.name = 'name'
        proxy.contragent__comment = 'contragent comment'
        proxy.chieff = 'chieff'
        proxy.lpu__comment = 'lpu comment'
        
        self.assertEqual(proxy.contragent.code, 'code')
        self.assertEqual(proxy.contragent.name, 'name')
        self.assertEqual(proxy.contragent.comment, 'contragent comment')
        self.assertEqual(proxy.lpu.chieff, 'chieff')
        self.assertEqual(proxy.lpu.comment, 'lpu comment')
        
        self.assertEqual(proxy.code, 'code')
        self.assertEqual(proxy.name, 'name')
        self.assertEqual(proxy.contragent__comment, 'contragent comment')
        self.assertEqual(proxy.chieff, 'chieff')
        self.assertEqual(proxy.lpu__comment, 'lpu comment')
        
        