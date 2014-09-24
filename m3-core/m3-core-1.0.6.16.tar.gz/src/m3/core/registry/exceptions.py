#coding:utf-8
'''
Created on 13.04.2011

@author: akvarats
'''

class GenericRegisterException(Exception):
    '''
    Общий класс исключения, который выбрасывается при некорректной работе
    с регистром
    '''
    pass

class WrongRegisterMeta(GenericRegisterException):
    '''
    Исключительная ситуация, которая выбрасывается в случае, если
    разработчиком была выполнена некорректная настройка регистра
    '''
    pass