#coding:utf-8
'''
Created on 28.10.2010

@author: akvarats
'''

from django.test import TestCase

from m3.data.caching import RuntimeCache
from cache import CustomCache0, CustomCache1

class RuntimeCacheTests(TestCase):
    '''
    Тесты для рантаймного кеша
    '''
    
    def test_infrastructure(self):
        '''
        Тестирование инфраструктуры контрола
        '''
        # блок тестов для _normalize_dimensions
        self.failUnlessEqual(RuntimeCache()._normalize_dimensions((0,1,)), (0,1,))
        self.failUnlessEqual(RuntimeCache()._normalize_dimensions(1), (1,))
        self.failUnlessEqual(RuntimeCache()._normalize_dimensions(None), ())
    
    def test_basics(self):
        '''
        Тестирование базовых операций
        '''
        self.failUnlessEqual(CustomCache0().get((0,1,)), (0,1,))
        self.failUnlessEqual(CustomCache0().get(2), (2,))
        self.failUnlessEqual(CustomCache0().get((0,1,)), (0,1,))
        
    def test_stat(self):
        '''
        Здесь тестируем статистику, т.е. дествительно ли данные берутся из кеша,
        либо же за ними необходимо лезть каждый раз в хендлер
        '''
        
        CustomCache0().drop_all()
        CustomCache0().clear_stat()
        
        CustomCache0().get(1)
        CustomCache0().get(1)
        CustomCache0().get(1)
        CustomCache0().get(1)
        
        self.failUnlessEqual(CustomCache0().stat.out_cache, 1)
        self.failUnlessEqual(CustomCache0().stat.in_cache, 3)
        
        CustomCache0().get(2)
        CustomCache0().get(2)
        
        self.failUnlessEqual(CustomCache0().stat.out_cache, 2)
        self.failUnlessEqual(CustomCache0().stat.in_cache, 4)
        
    def test_misc(self):
        '''
        Прочие тесты
        '''
        
        RuntimeCache().drop_all()
        CustomCache0().drop_all()
        
        # проверяем как работает RuntimeCache
        self.failUnlessEqual(RuntimeCache().get(1), (1,))
        # дергаем кастомный кеш и смотрим количество элементов в 
        # обоих тестах
        CustomCache0().get(1)
        self.failUnlessEqual(RuntimeCache().get_size(), 1)
        self.failUnlessEqual(CustomCache0().get_size(), 1)
        
        self.failUnlessEqual(CustomCache1().get(1),2)
        
    def test_hasdata(self):
        '''
        Проверка работы метода has_data
        '''
        
        RuntimeCache().drop_all()
        
        self.failUnlessEqual(RuntimeCache().has_data(1), False)
        RuntimeCache().set(1,1)
        self.failUnlessEqual(RuntimeCache().has_data(1), True)
        self.failUnlessEqual(RuntimeCache().has_data(2), False)
