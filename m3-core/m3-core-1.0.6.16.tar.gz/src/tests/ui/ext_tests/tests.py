#coding:utf-8
'''
Created on 21.11.2010

@author: akvarats
'''

from django.test import TestCase
from ui import SimpleWindow, SimpleEditWindow

class GenericExtUITests(TestCase):
    
    def test_0(self):
        pass
    
    
#===============================================================================
# Тесты механизма назначения нормальных наименований контролам
#===============================================================================
class QNamesTests(TestCase):
    '''
    Тесты, в которых проверяется работа механизма назначения псевдопостоянных
    наименований контролам.
    '''
    def test_simple_windows(self):
        '''
        Проверяем назначение имени для очень простой формы
        '''
        window = SimpleWindow()
        window.prepare_qnames()
        
        self.failUnlessEqual(window.qname, 'SimpleWindow')
        self.failUnlessEqual(window.ok_button.qname, 'SimpleWindow__ok_button')
        self.failUnlessEqual(window.cancel_button.qname, 'SimpleWindow__cancel_button')
        
    def test_simple_edit_window(self):
        window = SimpleEditWindow()
        window.prepare_qnames()
        
        self.failUnlessEqual(window.form.qname, 'SimpleEditWindow__form')
        self.failUnlessEqual(window.form.items[0].qname, 'SimpleEditWindow__named_field')
        self.failUnlessEqual(window.form.items[1].qname, 'SimpleEditWindow__form__ExtStringField0')
        self.failUnlessEqual(window.form.items[2].qname, 'SimpleEditWindow__form__ExtStringField1')
        self.failUnlessEqual(window.form.items[3].qname, 'SimpleEditWindow__form__ExtDateField0')