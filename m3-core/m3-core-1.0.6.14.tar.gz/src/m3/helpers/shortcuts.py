#coding:utf-8
'''
Created on 07.12.2010

@author: akvarats
'''

import inspect

from django.utils.importlib import import_module

def load_class(full_path):
    '''
    По полному строковому пути загружает и созвращает класс 
    '''
    # Получаем имя модуля и класса в нём
    dot = full_path.rindex('.')
    mod_name = full_path[:dot]
    pack_name = full_path[dot + 1:]
    # Пробуем загрузить
    mod = import_module(mod_name)
    clazz = getattr(mod, pack_name)
    return clazz

def get_instance(something):
    '''
    Возвращает экземпляр класса, который передан в something либо в виде
    строкового представления (полное квалифицирующее имя класса), либо
    в виде class-object, либо в виде самого экземпляра (который, собственно,
    и возвращается). 
    '''
    if isinstance(something, str):
        clazz = load_class(something)()
    elif inspect.isclass(something):
        clazz = something()
    else:
        clazz = something
    return clazz