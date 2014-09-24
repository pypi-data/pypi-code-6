# -*- coding: utf-8 -*-
'''
Модель истории должна иметь специальный формат, т.к. поля объявленные в ней используются 
в декораторе и зарезервированы
Пример:
class MyModel_History(BaseMyModel):
    history_object_id = models.IntegerField(db_index = True)
    history_time_stamp = models.DateTimeField(auto_now = True)
    
где BaseMyModel - абстрактный класс от которого наследована модель для которой ведется история

Пример подключения истории:
@history_support(MyModel_History)
class MyModel(BaseMyModel):
    pass
'''

from django.db import models
from django.db.models.signals import post_save

def history_support(history_model):
    '''
    Декоратор включающий поддержку истории для модели
    @param model_class: класс модели для которой включается ведение итории
    @param history_model: класс модели в который будет записываться история
    '''
    if not issubclass(history_model, models.Model):
        raise ValueError('Поддержка истории возможна только для моделей!')
            
    def wrapper(model_class):
        if not issubclass(model_class, models.Model):
            raise ValueError('Класс истории должен быть моделью!')
        
        def _on_save_history(sender, **kwargs):
            ''' Обработка события "после сохранения" модели '''
            instance = kwargs['instance']
            history_row = instance._history_model()
            history_row.history_object_id = instance.id
            # Копируем все поля таблицы в класс истории
            reserved_fields = ['id', 'history_object_id', 'history_time_stamp']
            for field in sender._meta.local_fields:
                attr = field.attname
                if not (attr in reserved_fields):
                    value = instance.__getattribute__(attr)
                    history_row.__setattr__(attr, value)
                    
            history_row.save()
        
        def get_history(self, reverse = False):
            ''' Возвращает QuerySet истории для текущей записи модели '''
            if not hasattr(self, '_history_model'):
                raise ValueError('Модель не поддерживает историю!')
            result = self._history_model.objects.filter(history_object_id = self.id)
            if reverse:
                return result.order_by('-history_time_stamp', '-id')
            else:
                return result.order_by('history_time_stamp', 'id')
        
        # Ссылка на модель истории, чтобы быстро предоставлять методы работы с историей
        if not hasattr(model_class, '_history_model'):
            model_class._history_model = history_model
            model_class.get_history = get_history
            post_save.connect(_on_save_history, model_class, weak = False)
        return model_class    

    return wrapper

#FIXME: Если в модели на поля наложена уникальность, то история будет падать. Нужен хак для убивания уникальности.
