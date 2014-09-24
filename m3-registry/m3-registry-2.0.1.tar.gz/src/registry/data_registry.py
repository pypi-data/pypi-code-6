#coding: utf-8
'''
Основной регистр сведений Платформы М3.

@author: akvarats
'''

import datetime

from django.db import models, transaction
from django.db.models.base import ModelBase


class BaseDataStoreModel(models.Model):
    '''
    Базовый класс для всех моделей, которые используются для хранения
    записей в регистрах сведений.
    '''
    drg_left  = models.DateTimeField() # левый конец интервала
    drg_right = models.DateTimeField() # правый конец интервала
    drg_center = models.DateTimeField() # момент времени, на который происходит сохранение значения
    
    class Meta:
        abstract = True


class DataRegistry(object):
    '''
    Базовый класс для регистров сведений.
    
    Создание прикладного регистра выполняется следующим образом:
    <code>
    # myapp/models.py
    from m3.core.registry import DataRegistry, BaseDataStoreModel
    
    class MyDataModel(BaseDataStoreModel):
        # данная модель используется для хранения информации в регистре
        field1 = ...
        field2 = ...
    
    class MyDataRegistry(DataRegistry):
        model = MyDataModel
        dimentions = ['field1',]
        resources = ['field2',]
        period = DataRegistry.PERIOD_DAY
    </code>
    '''
    
    #===========================================================================
    # Атрибуты для работы конкретного регистра 
    #===========================================================================
    model = None
    dimentions = []
    resources = []
    period = 0 # PERIOD_INFTY = 0
    
    #===========================================================================
    # Внутренние константы регистра
    #===========================================================================
    PERIOD_INFTY = 0 # в регистре нет периодичности и нет динамически хранящихся
    PERIOD_SECOND = 1 # до секунд
    PERIOD_MINUTE = 2
    PERIOD_HOUR = 3
    PERIOD_DAY = 4
    PERIOD_MONTH = 5
    PERIOD_QUARTER = 6
    PERIOD_YEAR = 7
    
    #===========================================================================
    # Операции вставки данных в регистр
    #===========================================================================
    @classmethod
    @transaction.commit_on_success
    def insert(cls, data, date = None):
        '''
        Выполняет сохранение данных в регистре сведений. 
        
        @param data: объект, который содержит данные для сохранения в регистр.
                     Это может быть либо 1) объект модели хранения данных регистра,
                     либо 2) словарь, ключами которого являются имена полей из модели хранения,
                     либо 3) объект любого класса, у которого есть атрибуты с именами
        
        @param date: дата/время актуальности сведений
        @param none_options
        '''
        
        if cls.period != DataRegistry.PERIOD_INFTY and not date:
            raise Exception(u'Не задана дата при вставке данных в периодический регистр')
        
        # нормализуем переданные дату и время 
        reg_date = cls._normdate(date) 
        
        # временный объект для корректного хранения вставляемых данных
        query_model = cls._get_model_object(data, model=DataRegistry.QueryDataHolder())
        
        query_affected_models = cls.model.objects
        for dim_field in cls.dimentions:
            if getattr(query_model, dim_field, None) != None:
                query_affected_models = query_affected_models.filter(**{dim_field: getattr(query_model, dim_field, None)})
        
        if cls.period != DataRegistry.PERIOD_INFTY:
            query_affected_models = query_affected_models.filter(drg_left__lte = reg_date).filter(drg_right__gte = reg_date)
        query_affected_models = query_affected_models.order_by('drg_center')
        
        affected_models = list(query_affected_models)
        
        if cls.period != DataRegistry.PERIOD_INFTY:
            left_bound = datetime.datetime.min
            right_bound = datetime.datetime.max
            model_to_save = None
            for affected_model in affected_models:
                if affected_model.drg_center < reg_date:
                    affected_model.drg_right = reg_date
                    affected_model.save()
                    left_bound = affected_model.drg_center if affected_model.drg_center > left_bound else left_bound
                elif affected_model.drg_center > reg_date:                    
                    affected_model.drg_left = reg_date
                    affected_model.save()
                    right_bound = affected_model.drg_center if affected_model.drg_center < right_bound else right_bound
                elif affected_model.drg_center == reg_date:
                    model_to_save = affected_model
            model_to_save = cls._get_model_object(data, model_to_save)
            model_to_save.drg_left = left_bound
            model_to_save.drg_center = reg_date
            model_to_save.drg_right = right_bound
            model_to_save.save()
        else:
            # регистр у нас непериодический
            if affected_models:
                for affected_model in affected_models:
                    affected_model = cls._get_model_object(data, affected_model)
                    affected_model.save()
            else:
                affected_model = cls._get_model_object(data)
                affected_model.drg_left = datetime.datetime.min
                affected_model.drg_center = datetime.datetime.min
                affected_model.drg_right = datetime.datetime.max 
                affected_model.save()
        
    @classmethod
    def query(cls, dimentions, date = None, next = False):
        '''
        Возвращает данные из регистра.
        '''
        # временный объект для корректного хранения вставляемых данных
        query_model = cls._get_model_object(dimentions)
        
        query = cls.model.objects
        for dim_field in cls.dimentions:
            if getattr(query_model, dim_field, None) != None:
                query = query.filter(**{dim_field: getattr(query_model, dim_field, None)})
        
        if cls.period != DataRegistry.PERIOD_INFTY and date:
            reg_date = cls._normdate(date)
            if next:
                query = query.filter(drg_left__lt = reg_date).filter(drg_center__gte = reg_date)
            else:
                query = query.filter(drg_center__lte = reg_date).filter(drg_right__gt = reg_date)
        
        query = query.order_by('drg_center')
        return query
    
    @classmethod
    @transaction.commit_on_success
    def remove(cls, dimentions, date = None):
        '''
        Процедура удаления записей регистра. Процедура выполняет удаление записей на основе
        переданных в dimentions ключевых значений разрезов. В случае, если указана
        дата, то производится удаление данных, действительных на данную дату.
        
        @param dimentions: словарь, либо объект, атрибуты которого
                           характеризуют удаляемые сведения
        @param date: дата, на которую удаляются сведения
        '''
        if cls.period == DataRegistry.PERIOD_INFTY:
            # в случае непериодического регистра просто выполняем
            # удаление записей
            cls._get_query_by_dimentions(dimentions).delete()
        else:
            # в случае периодического регистра помимо удаления указанных
            # записей необходимо пересчитать даты начала и окончания
            # у смежных записей 
    
            reg_date = cls._normdate(date)
        
            if cls.period != DataRegistry.PERIOD_INFTY and not reg_date:
                raise Exception(u'Не указана дата при удалении данных из периодического регистра')
             
            # получаем список записей для удаления
            query_delete = cls._get_query_by_dimentions(dimentions).filter(drg_center = reg_date)
                        
            for model in query_delete:
                # обновляем правую границу у смежной слева записью
                cls._get_query_by_dimentions(dimentions).filter(drg_right = reg_date).update(drg_right = model.drg_right)
                # обновляем левую границу у смежной справа записью
                cls._get_query_by_dimentions(dimentions).filter(drg_left = reg_date).update(drg_left = model.drg_left)
            
            cls._get_query_by_dimentions(dimentions).filter(drg_center = reg_date).delete()
                
        
    
    @classmethod
    def change(cls, dimentions, date = None, new_resources = None, new_date = None):
        pass
    
    @classmethod
    def _get_model_object(cls, data, model = None):
        
        model_obj = model if model else cls.model()
        
        fields = []
        fields.extend(cls.dimentions)
        fields.extend(cls.resources)
        if isinstance(data, dict):
            for field_name in fields:
                if data.has_key(field_name):
                    setattr(model_obj, field_name, data[field_name])
        else:
            for field_name in fields:
                if hasattr(data, field_name):
                    setattr(model_obj, field_name, getattr(data, field_name))
        
        return model_obj
    
    @classmethod
    def _normdate(cls, date):
        '''
        Метод нормализует дату таким образом, чтобы
        она отражала 
        '''
        if not date:
            return None        
        if cls.period == DataRegistry.PERIOD_SECOND:
            return datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
        if cls.period == DataRegistry.PERIOD_MINUTE:
            return datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, 0)
        if cls.period == DataRegistry.PERIOD_HOUR:
            return datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
        if cls.period == DataRegistry.PERIOD_DAY:
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        if cls.period == DataRegistry.PERIOD_MONTH:
            return datetime.datetime(date.year, date.month, 1, 0, 0, 0)
        if cls.period == DataRegistry.PERIOD_QUARTER:
            if date.month < 4:
                return datetime.datetime(date.year, 1, 1, 0, 0, 0)
            if date.month < 7:
                return datetime.datetime(date.year, 4, 1, 0, 0, 0)
            if date.month < 10:
                return datetime.datetime(date.year, 7, 1, 0, 0, 0)
            return datetime.datetime(date.year, 10, 1, 0, 0, 0)
        if cls.period == DataRegistry.PERIOD_YEAR:
            return datetime.datetime(date.year, 1, 1, 0, 0, 0)
        
        return date
    
    @classmethod
    def _get_query_by_dimentions(cls, dimentions):
        result_query = cls.model.objects
        
        query_model = cls._get_model_object(dimentions)
        for dim_field in cls.dimentions:
            if getattr(query_model, dim_field, None) != None:
                result_query = result_query.filter(**{dim_field: getattr(query_model, dim_field, None)})
                
        return result_query
        