#coding:utf-8
'''
Различные хендлеры для подсистемы mie

@author: akvarats
'''

from m3.helpers.logger import logging

from cache import MieCache

def simple_mei_pre_delete(sender, instance, *args, **kwargs):
    '''
    Функция удаления extenders-моделей при удалении
    основной модели приложения
    '''
    try:
        extenders = MieCache().get_extenders(sender)
        for ext_model in extenders:
            ext_model.objects.filter(**{ext_model._mie_meta.primary_field: instance.id}).delete()
    except:
        logging.exception(u'Не удалось удалить MIE объекты')
