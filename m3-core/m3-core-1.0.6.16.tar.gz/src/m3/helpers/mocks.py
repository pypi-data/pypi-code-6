#coding:utf-8
'''
Модуль для обеспечения имитационного поведения API функций 

Created on 21.03.2011

@author: akvarats
'''
import inspect

def fmock(mock=None):
    '''
    Декоратор, который используется для обеспечения имитации вызова
    реальной API функции.
    
    @param mock: callable объект, который будет вызван вместо
        обернутой функции.
        
    В случае если mock=None, то декоратор попытается найти в текущем
    относительно оборачиваемой функции метод с именем 'mock_' + её имя.
    Если у декоратора не получится определить, чо же там вызывать,
    то будет выполнена исходная функция
    
    Пример использования:
    
    def mock_func(a):
        return a + 100
     
    @fmock() # или @fmock(mock_func) 
    def f(a):
        return a + 10
        
    print func(1) # напечатает 101
    '''
    def inner(f):
        def wrapper(*args, **kwargs):
            func = mock
            if not func:
                func = getattr(inspect.getmodule(f), 'mock_' + f.__name__, None)
                if not callable(func):
                    func = f     
            return func(*args, **kwargs)
        return wrapper
    return inner


class QuerySetMock(object):
    '''
    Mock класс, который может использоваться для создания объектом, замещающих
    джанговские queryset'ы.
    '''
    def __init__(self, objects):
        '''
        @param objects: список объектов, которые будут отдаваться при 
            обращении к данному mock-queryset'у
        '''
        self.objects = objects
    
    
    #===========================================================================
    # Замещающие функции-пустышки
    #===========================================================================
    def filter(self, *args, **kwargs):
        pass
    
    def select_replated(self, *args, **kwargs):
        pass
        
    def order_by(self, *args, **kwargs):
        pass