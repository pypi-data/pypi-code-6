#coding:utf-8
'''
Created on 06.11.2010

Содержит менеджер, который разруливает механизм

@author: akvarats
'''

from m3.data.caching import RuntimeCache

from exceptions import DropMieCacheException

class MieCache(RuntimeCache):
    '''
    Кеш, который хранит в себе все связи моделей.
    
    Доступно следующее API для работы с классом:
    * add_extender: добавляет в кеш связку "первичная модель" - расширение
    * get_extenders: возвращяет все расширения для указанной первичной модели
    '''
    def drop(self, dimensions):
        '''
        Переопределенный метод частичного сброса кеша. 
        
        Выдает исключение, посколько с MieCache такое делать нельзя
        '''
        raise DropMieCacheException()
    
    def drop_all(self):
        '''
        Переопределенный метод полного сброса кеша.
        
        Выдает исключение, поскольку с MieCache такое делать нельзя
        '''
        raise DropMieCacheException()
    
    def get_extenders(self, primary_model):
        '''
        Возвращает расширения, объявленные для указанной первичной модели 
        '''
        return self.get(primary_model, [])
    
    def add_extender(self, primary_model, extender_model):
        '''
        Добавляет в кеш расширение extender_model для указанной первичной модели primary_model 
        '''
        extenders_list = self.get(primary_model, None)
        if extenders_list == None:
            extenders_list = []
            self.set(primary_model, extenders_list)
        # TODO: надо понять, нужно ли блокировать одновременный доступ к 
        # 
        if not extender_model in extenders_list:
            extenders_list.append(extender_model)
            