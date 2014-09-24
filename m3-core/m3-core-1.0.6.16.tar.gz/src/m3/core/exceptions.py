#coding:utf-8
'''
Created on 29.11.2010

Модуль с исключительными ситуациями для Платформы М3 и создаваемых на ней приложениях

@author: akvarats
'''

class ApplicationLogicException(Exception):
    '''
    Исключительная ситуация уровня бизнес-логики приложения.
    '''
    
    def __init__(self, message):
        '''
        '''
        # Это исключение плохо подвергается pickle! пришлось дописать.
        # пруф: http://bugs.python.org/issue1692335  http://bugs.python.org/issue13751
        Exception.__init__(self, message)
        self.exception_message = message
    
    def __str__(self):
        '''
        '''
        return self.exception_message
    
class RelatedError(Exception):
    '''Исключение для получения связанных объектов.'''
    pass
