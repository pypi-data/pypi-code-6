#coding: utf-8
'''
Created on 06.11.2010

Исключения, выбрасываемые из m3.data.mie

@author: akvarats
'''

class MieException(Exception):
    '''
    Некоторое исключение.
    '''
    pass

class NoMieMetaException(MieException):
    '''
    Исключение, выбрасываемое в случае, если для расширяющей
    модели не задана MieMeta 
    '''
    pass

class IncompleteMieMetaException(MieException):
    '''
    Исключение, выбрасываемое в случае, если для расширяющей
    модели MieMeta задана неполностью
    '''
    pass

class DropMieCacheException(MieException):
    '''
    Возникает при попытке сброса значений в кеше Mie.
    
    Этот кеш никогда дропать нельзя!
    '''
    pass