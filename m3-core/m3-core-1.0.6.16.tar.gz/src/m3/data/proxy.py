#coding: utf-8
'''
Модуль, который обеспечивает работу с прокси объектами.

Created on 27.07.2011

@author: akvarats
'''

import re

from django.db import models as django_models

# для преобразований 
_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')

class Proxy(object):
    
    # список моделей (внутренних объектов моделей)
    proxy_models = []
    
    # карта соответствия внешних атрибутов данного класса и атрибутов
    # моделей
    proxy_map = {} 
    
    # ключи для связывания объектов моделей, указанных в proxy_models
    # между собой
    proxy_keys = {}
    
    
    #===========================================================================
    # Набор методов, которые предоставляют интерфейс доступа к 
    # динамическим атрибутам внутренних моделей прокси-объекта
    #===========================================================================
    
    def _models(self):
        '''
        Возвращает внутренний список моделей, которые образуют данный
        прокси объект
        '''
        if not isinstance(self.proxy_models, list):
            # считаем, что прокси строится на основе только одной модели
            # для обеспечения общего интерпретации списка моделей
            self.__dict__['proxy_models'] = [self.proxy_models,]
        
        # проверяем, что данные для списка моделей заданы в нужном формате
        # список моделей должен состоять из кортежей вида (класс_модели, 
        # название_экземпляра_модели_в_прокси_объекте
        
        cleaned_proxy_models = []
        
        for i in range(0, len(self.proxy_models)):
            if not isinstance(self.proxy_models[i], tuple):
                cleaned_proxy_models.append((self.proxy_models[i], self._convert_to_underscore(self.proxy_models[i].__name__), ))
            else:
                cleaned_proxy_models.append(self.proxy_models[i])
            # если атрибут прокси-объекта отсутствует, то записываем его
            if not hasattr(self, self.proxy_models[i][1]):
                setattr(self, self.proxy_models[i][1], None)
        
        return self.__dict__['proxy_models']
    
    def _map(self):
        '''
        Возвращает таблицу соответствия внешних полей прокси-класса и внутренних 
        полей моделей.
        
        Метод гарантирует единообразие представления соответствия полей вне 
        зависимости от вариантов их задавания.
        
        Внимание! Метод при определенных условиях может вызывать создавать
        экземпляры классов из списка моделей.
        '''
        if not self.proxy_map:
            # карта полей не задана, пытаемся её создать
            self.__dict__['proxy_map'] = {}
            
            # список атрибутов всех моделей. представлен в виде кортежа
            # ("имя поля", модель хранения атрибута, "внешнее имя поля")
            all_attributes = []
            
            # собираем общий список атрибутов
            for model, proxy_attribute in self._models():
                
                model_attrs = []
                if isinstance(model, django_models.Model):
                    model_attrs.extend([field.name for field in model._meta.fields])
                elif hasattr(model, 'attributes') and callable(model.attributes):
                    model_attrs.extend(model().attributes())
            
                all_attributes.extend([(attr, model, attr) for attr in model_attrs])
                
            # нормализуем список, убирая дублирующиеся элеметы
            for attr_name, model, external_name in all_attributes:
                dupl = filter(lambda x: x[0] == attr_name, all_attributes)
                if len(dupl) > 1:
                    map(lambda x: (x[0], x[1], '%s__%s' % (x[1].__name__, x[0])), all_attributes)
                
            for attr_name, model, external_name in all_attributes:
                self.proxy_map[external_name] = (attr_name, self._convert_to_underscore(model.__name__))
                
            self.__dict__['proxy_map'] = all_attributes
                
        return self.__dict__['proxy_map']
    
    def _keys(self):
        '''
        Возвращает описание связей между участвующими в образовании 
        текущего proxy-объекта моделями
        '''
        return self.keys
    
    def __getattr__(self, name):
        '''
        Обеспечение доступа на чтение к атрибутам верхнего уровня класса
        '''
        if name in ['proxy_models', 'proxy_map', 'proxy_keys']:
            # проставление значений зарезервированные на уровне класса атрибуты
            return self.__dict__.get(name, self.__class__.__dict__.get(name, None))
        
        
        inner_attr = self._map().get(name, None)
        if not inner_attr:
            return None
        
        return getattr(getattr(self, inner_attr[0]), inner_attr[1])
    
    
    def __setattr__(self, name, value):
        '''
        Обеспечение доступа на запись к атрибутам верхнего уровня класса
        '''
        
        if name in ['proxy_models', 'proxy_map', 'proxy_keys']:
            # проставление значений зарезервированные на уровне класса атрибуты
            self.__dict__[name] = value
            return self.__dict__[name]
            
        inner_attr = self._map().get(name, None)
        if not inner_attr:
            return None
        
        return setattr(getattr(self, inner_attr[0]), inner_attr[1], value)
        
    #===========================================================================
    # Внешний интерфейс объектов класса
    #===========================================================================
    def attributes(self):
        '''
        Возвращает список атрибутов, которые доступны у объекта данного класса
        '''
        return self._map.keys()
    
    
    @staticmethod
    def create(models, map=[], keys={}):
        '''
        Фабрика для создания экземпляров прокси-объектов на лету
        '''
        proxy = Proxy()
        
        proxy.proxy_models = models
        proxy.proxy_map = map
        proxy.proxy_keys = keys
        
        return proxy
    
    #===========================================================================
    # Вспомогательные методы
    #===========================================================================
    def _convert_to_underscore(self, name):
        s1 = _first_cap_re.sub(r'\1_\2', name)
        return _all_cap_re.sub(r'\1_\2', s1).lower()
        