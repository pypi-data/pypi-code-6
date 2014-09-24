#coding:utf-8
'''
Created on 06.11.2010

@author: akvarats
'''

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import pre_delete

from cache import MieCache
from exceptions import NoMieMetaException, IncompleteMieMetaException
from handlers import simple_mei_pre_delete

class BaseMIEMetaclass(ModelBase):
    '''
    Базовый метакласс для расширений моделей
    '''
    def __new__(cls, name, bases, attrs):
        
        klass = super(BaseMIEMetaclass, cls).__new__(cls, name, bases, attrs)
        
        abstract = getattr(getattr(klass, '_meta', None), 'abstract', False)
        
        if abstract:
            '''
            Анализ MieMeta работает только для неабстрактных моделей
            '''
            return klass
            
        klass._check_mie_meta()
        
        # устанавливаем текущий MieMeta в атрибут _mie_meta,
        # как, собственно, и делается в джанге 
        setattr(klass, '_mie_meta', klass.MieMeta)
        # регистрируем расширение ведущей модели
        MieCache().add_extender(klass._mie_meta.primary_model, klass)
        # присоединяем хендлеры к операциям над моделями
        klass._connect_handlers()
        return klass
    
    
    def _check_mie_meta(cls):
        '''
        Модуль проверки MieMeta для модели
        '''
        # собираем метаданные о моделях
        mie_meta = getattr(cls, 'MieMeta', None)
        if not mie_meta:
            raise NoMieMetaException(u'Для класса ' + str(cls) + u' не задана MieMeta.')
        primary_model = getattr(mie_meta, 'primary_model', None)
        if not primary_model:
            raise IncompleteMieMetaException(u'Для класса ' + str(cls) + u' в MieMeta не задан атрибут primary_model.')
        # пытаемся понять, как называется поле-ссылка на первичную модель 
        primary_field = getattr(mie_meta, 'primary_field', 'mie_primary')
        setattr(mie_meta, 'primary_field', primary_field)
        if not hasattr(cls, primary_field):
            raise IncompleteMieMetaException(u'Для модели ' + str(cls) + u' не задано поле-ссылка на расширяемую модель.')
    
        
    def _connect_handlers(cls):
        '''
        Метод, который должен быть переопределен в дочерних классах.
        
        Должен выполнять присоединение хендлеров к различным операциям
        над первичными моделями
        '''
        pass
        
class SimpleMIEMetaclass(BaseMIEMetaclass):
    '''
    Метакласс для моделей, которые расширяют другие модели
    '''
    def __new__(cls, name, bases, attrs):
        klass = super(SimpleMIEMetaclass, cls).__new__(cls, name, bases, attrs)
        return klass
    
    
    def _connect_handlers(cls):
        '''
        Переопределенный метод присоединения хендлеров к моделям
        '''
        # назначаем хендлер который при удалении ведущей модели
        # почистит все низлежащие
        pre_delete.connect(simple_mei_pre_delete, cls._mie_meta.primary_model, weak=True)
        
    
class DatedMIEMetaclass(BaseMIEMetaclass):
    
    def __new__(cls, name, bases, attrs):
        klass = super(DatedMIEMetaclass, cls).__new__(cls, name, bases, attrs)    
        return klass
    
    
    def _check_mie_meta(cls):
        super(DatedMIEMetaclass, cls)._check_mie_meta()
        mie_meta = getattr(cls, 'MieMeta', None)
        date_field = getattr(mie_meta, 'date_field', None)
        if not date_field:
            raise IncompleteMieMetaException(u'Для класса ' + str(cls) + u' в MieMeta не задан атрибут date_field.')
        # TODO: надо разобраться, почему две нижние строчки косячили
        # на тестовом случае
        # if not hasattr(cls, date_field):
        #    raise IncompleteMieMetaException(u'Для модели ' + str(cls) + u' не задано поле даты.')
        
    def _connect_handlers(cls):
        pass
    
class SimpleModelExtender(models.Model):
    '''
    Базовый класс для простых расширений информации по другой модели
    '''
    __metaclass__ = SimpleMIEMetaclass
    
    class Meta:
        abstract = True
    
class DatedModelExtender(models.Model):
    '''
    Базовый класс для моделей, которые расширяют информацию по другой модели 
    периодическим способом
    '''
    __metaclass__ = DatedMIEMetaclass
    
    class Meta:
        abstract = True
    