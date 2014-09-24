#coding:utf-8
'''
Created on 14.07.2011

@author: akvarats
'''
# данные импорты для использования вовне системы
from domain import TimeoutAutoRelease, MutexQuery
from backends import ModelMutexBackend
#from helpers import get_backend

def get_backend(mutex_id):
    return ModelMutexBackend()

def capture_mutex(mutex_id, owner=None, auto_release=TimeoutAutoRelease(timeout=300), status_data=None):
    '''
    Устанавливает семафор с таймаутом в 300 секунд (5 минут) по умолчанию
    '''
    return get_backend(mutex_id).capture_mutex(mutex_id, owner, auto_release, status_data)

def release_mutex(mutex_id, owner=None):
    '''
    Освобождает семафор
    '''
    return get_backend(mutex_id).release_mutex(mutex_id, owner)

def request_mutex(mutex_id, owner=None):
    '''
    Проверяет, свободен ли семафор. Информация возвращается в виде кортежа
    (Состояние, Статусные данные,)
    '''
    return get_backend(mutex_id).request_mutex(mutex_id, owner)


def get_mutex_list(mutex_query=MutexQuery()):
    '''
    Возвращает список семафоров с условием отбора,
    заданным в mutex_query
    '''
    return []

