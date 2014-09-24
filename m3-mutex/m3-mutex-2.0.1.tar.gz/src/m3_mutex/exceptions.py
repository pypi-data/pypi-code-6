#coding:utf-8
'''
Created on 20.07.2011

@author: akvarats
'''

class MutexBusy(Exception):
    '''
    Исключительная ситуация, возникающая при попытке
    захвата семафора, который уже захвачен другим владельцем
    '''
    pass
