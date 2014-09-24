#coding:utf-8
'''
Кеши объектов приложения для подсистемы рабочих потоков

Created on 10.03.2010

@author: akvarats
'''

from django.utils.datastructures import SortedDict
from django.conf import settings

import sys
import os
import threading

class WorkflowCache(object):
    '''
    Кэш объектов workflow для приложения
    '''
    __shared_state = dict(
        workflow_store = SortedDict(),
        loaded = False,
        write_lock = threading.RLock() 
    )
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def _populate(self):
        '''
        Загружает информацию о классах рабочих процессов
        в текущий кэш
        '''
        if self.loaded:
            return
        self.write_lock.acquire()
        try:
            if self.loaded:
                return
        finally:
            self.write_lock.release()
    
    def workflow_cache_ready(self):
        '''
        Возвращает True в случае если кэш полностью прогружен
        '''
        return self.loaded
            
    def get_workflow(self, workflow_name, workflow_version = -1):
        '''
        Возвращает тип рабочего процесса, зарегистрированный с именем workflow_name
        '''
        self._populate()
        try:
            pass
        except:
            pass
        
cache = WorkflowCache()

get_workflow = cache.get_workflow 