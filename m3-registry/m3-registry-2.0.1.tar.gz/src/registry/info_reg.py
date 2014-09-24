# -*- coding: utf-8 -*-
from django.db.models.base import ModelBase
from django.db import models
import datetime
import copy

class InformationRegistryMeta(ModelBase):
    '''
    Метакласс регистра сведений. Предназначен для создания полей регистра на ходу, исходя из
    указанных в нём управляемых моделей и полей
    '''
    def __new__(cls, name, bases, dct):
        super_new = super(InformationRegistryMeta, cls).__new__
        clazz = super_new(cls, name, bases, dct)
        
        # Если создаваемый класс не наследуется от регистра, то он идет лесом
        for base in bases:
            if base.__name__ == 'BaseInformationRegistry':
                break
        else:
            return clazz
        
        if (len(clazz.managed_models) == 0) or (hasattr(clazz, '_fields_conformity')):
            return clazz
        
        # Получаем все экземпляры полей, имена моделей и имена полей
        ignored = ['id']
        all_fields = []
        for model in clazz.managed_models:
            for field in model._meta.local_fields:
                if field.attname not in ignored:
                    all_fields.append((field, model.__name__, field.name))
        
        # Формируем список полей которые будут созданы в регистре:
        # Класс, полное имя, соответствие
        fields_to_make = []
        fields_conformity = {}
        m_fields = clazz.managed_fields
        if len(m_fields) == 0:
            # Берем все поля управляемой модели
            for field_obj, model_name, field_name in all_fields:
                fields_to_make.append((field_obj, field_name))
                fields_conformity[field_name] = field_name
        elif isinstance(m_fields, list) or isinstance(m_fields, tuple):
            # Берем первое попавшееся совпадающее имя
            for name in m_fields:
                for field_obj, model_name, field_name in all_fields:
                    if name == field_name:
                        fields_to_make.append((field_obj, name))
                        fields_conformity[name] = name
                        break
                else:
                    raise ValueError(u'Поле %s не найдено в указанных моделях %s' % (name, m_fields))
        elif isinstance(m_fields, dict):
            # Уже есть строгое соответствие
            for key, value in m_fields.items():
                m_name, f_name = key.split('.')
                for field_obj, model_name, field_name in all_fields:
                    if (m_name == model_name) and (f_name == field_name):
                        fields_to_make.append((field_obj, value))
                        fields_conformity[key] = value
                        break
                else:
                    raise ValueError(u'Имя модели и поля %s.%s указанное в managed_fields \
                                     не найдены в managed_models %s' % (m_name, f_name, m_fields))
        else:
            raise TypeError(u'Неверный тип managed_fields')
        
        clazz._fields_conformity = fields_conformity
        
        # Создаем такие же поля, но не клонируем, т.к. нужны лишь некоторые свойства
        for field, name in fields_to_make:
            new_field = copy.copy(field)
            # Нужно грохнуть уникальность чтобы не сбивать вставку истории
            new_field.primary_key = False
            new_field._unique = False
            new_field.contribute_to_class(clazz, name)
         
        return clazz
        
def check_obj(obj):
    if not isinstance(obj, models.Model):
        raise TypeError(u'Объект по которому запрашивается история должен быть наследником models.Model')


class BaseInformationRegistry(models.Model):
    ''' Базовый класс для создания регистра сведений '''
    __metaclass__ = InformationRegistryMeta
    managed_models = []
    managed_fields = []
    
    history_time_stamp = models.DateTimeField(db_index = True)
    history_object_id = models.IntegerField(db_index = True)
    
    def mapping(self, *args, **kwargs):
        '''
        Раскидывает данные по полям регистра в порядке определенном пользователем
        Предпологается что в args передаются объекты, а в kwargs отдельные поля
        '''
        # Попробуем дернуть нужные нам поля из каждого объекта
        for obj in args:
            if not isinstance(obj, tuple(self.managed_models)):
                raise TypeError(u'Нужно передавать экземпляр модели')
            for orig_name, pseudonym in self._fields_conformity.items():
                if '.' in orig_name:
                    # Нужно точное соответствие
                    model_name, field_name = orig_name.split('.')
                    if obj.__class__.__name__ == model_name:
                        value = obj.__getattribute__(field_name)
                        self.__setattr__(pseudonym, value)
                elif hasattr(obj, orig_name):
                    # Подойдет любой
                    value = obj.__getattribute__(orig_name)
                    self.__setattr__(pseudonym, value)
        
        # Попробуем заполнить по полям из словаря
        for name, value in kwargs.items():
            if not hasattr(self, name):
                raise AttributeError(u'Регистр не содержит атрибут с именем %s' % name)
            if name != 'id':
                self.__setattr__(name, value)
        
        # Откуда-то нужно достать id
        if not self.history_object_id:
            if len(args) > 0:
                self.history_object_id = args[0].id
            else:
                self.history_object_id = kwargs['id']
        
        self.save()
    
    @classmethod
    def add_object(cls, *args, **kwargs):
        new_record = cls()
        new_record.history_time_stamp = kwargs.pop('date', datetime.datetime.now())
        cls.mapping(new_record, *args, **kwargs)
        return new_record
    
    @classmethod
    def get_object(cls, obj, date = None):
        '''
        Получение записи регистра по дате и объекту
        '''
        check_obj(obj)
        date = date or datetime.datetime.now()
        result = cls.objects.order_by('-history_time_stamp')
        res = result.filter(history_time_stamp__lte = date, history_object_id = obj.id)
        if res:
            return res[0]
        else:
            return None
    
    @classmethod
    def get_history(cls, obj, reverse = False):
        check_obj(obj)
        result = cls.objects.filter(history_object_id = obj.id)
        if reverse:
            return result.order_by('-history_time_stamp', '-id')
        else:
            return result.order_by('history_time_stamp', 'id')
    
    class Meta:
        abstract = True

#FIXME: 
#TODO: Сделать возможность хранения нескольких id моделей
#TODO: Сделать возможность хранения нескольких id моделей
