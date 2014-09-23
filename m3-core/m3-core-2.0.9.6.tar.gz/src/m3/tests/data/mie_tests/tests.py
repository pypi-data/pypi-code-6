#coding:utf-8
'''
Created on 06.11.2010

@author: akvarats
'''

from django.test import TestCase

from m3.data.mie import MieCache
from models import MainModel, MainModelSimpleExtender1,\
                              MainModelSimpleExtender2,\
                              MainModelDatedExtender1

class SimpleMIETests(TestCase):
    
    def test_meta(self):
        '''
        Тесты на правильную отработку MieMeta в моделях
        '''
        # в расширяемой модели ._mie_meta.primary_model должен указывать на первичную модель
        self.failUnlessEqual(MainModelSimpleExtender1._mie_meta.primary_model, MainModel)
        
        # проверяем как модели зарегистрировались в mie_cache
        # в models.py для MainModel определяется два MIE расширения
        extenders = MieCache().get_extenders(MainModel)
        
        self.failUnlessEqual(len(extenders), 3)
        self.failUnless(MainModelDatedExtender1 in extenders)
        self.failUnless(MainModelSimpleExtender1 in extenders)
        self.failUnless(MainModelSimpleExtender2 in extenders)