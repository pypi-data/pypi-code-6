#coding:utf-8
'''
Created on 22.07.2011

@author: akvarats
'''
import m3_mutex

from m3.ui import actions
from m3.core.middleware import get_thread_data

class MutexActionPack(actions.ActionPack):
    '''
    '''
    url = '/mutex'
    shortname = 'mutex-pack'
    
    def __init__(self):
        super(MutexActionPack, self).__init__()
        self.actions.extend([CaptureMutexOkAction(),
                             CaptureMutexFailAction(),
                             RequestMutexAction(),
                             RequestStatusDataAction(),
                             ReleaseMutexOkAction(),
                             ReleaseMutexFailAction(),
                             ShortCaptureMutexAction(),])
    
    def pre_run(self, request, context):
        '''
        '''
        # выводим информацию для отладки методом сурового взгляда
        print 'mutex tests. url: %s, session_key: %s' % (request.session.session_key, request.path)
        # дамипируем данные из thread-locals
        #print 'thread data:'
        #print get_thread_data().dump()
        
        

class MutexActionBase(actions.Action):
    '''
    Базовый класс для запросов к подсистеме 
    '''
    def context_declaration(self):
        return [actions.ACD(name='mutex_group', type=str, required=True, default=''),
                actions.ACD(name='mutex_mode', type=str, required=True, default=''),
                actions.ACD(name='mutex_id', type=str, required=True),
                actions.ACD(name='status_data', type=str, required=True, default=''),]

class CaptureMutexOkAction(MutexActionBase):
    '''
    Действие, которое выполняет захват свободного семафора mutex1
    '''
    
    url = '/capture-ok'
    shortname = 'mutex.capture-ok'

    def run(self, request, context):
        ''' 
        ''' 
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        # 1. захватываем семафор
        m3_mutex.capture_mutex(mutex_id, status_data=context.status_data)
        
        # 2. проверяем состояние захваченного семафора
        state, _ = m3_mutex.request_mutex(mutex_id)
        
        if state != m3_mutex.MutexState.CAPTURED_BY_ME:
            return actions.TextResult(u'После выполнения операции блокировки семафор должен находиться в состоянии "Заблокирован текущим владельцем".')
        
        return actions.TextResult('ok')
    
class CaptureMutexFailAction(MutexActionBase):
    '''
    Запрос, который пытается захватить семафор, который должен быть 
    занят другим владельцем.
    '''
    
    url = '/capture-fail'
    shortname = 'mutex.capture-fail'
    
    def run(self, request, context):
        '''
        '''
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        # 0. проверяем, что семафор должен находиться в состоянии "Занят не нами"
        state, _ = m3_mutex.request_mutex(mutex_id)
        if state != m3_mutex.MutexState.CAPTURED_BY_OTHER:
            return actions.TextResult(u'Первоначально, семафор должен находиться в состоянии "Занят другим владельцем".')
        
        try:
            m3_mutex.capture_mutex(mutex_id)
        except m3_mutex.MutexBusy:
            return actions.TextResult('ok')
        
        return actions.TextResult(u'Удалось захватить активный семафор с другим владельцем.')
    
class RequestMutexAction(MutexActionBase):
    '''
    Действие, которое проверяет состояние заблокированного нами же семафора mutex1
    '''
    
    url = '/request'
    shortname = 'mutex.request'
    
    def run(self, request, context):
        '''
        '''
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        # 0. проверяем, что семафор должен находиться в состоянии "Занят не нами"
        state, _ = m3_mutex.request_mutex(mutex_id)
        
        name_map = {m3_mutex.MutexState.FREE: 'FREE',
                    m3_mutex.MutexState.CAPTURED_BY_ME: 'CAPTURED_BY_ME',
                    m3_mutex.MutexState.CAPTURED_BY_OTHER: 'CAPTURED_BY_OTHER',}
        
        return actions.TextResult(name_map[state])
    

class RequestStatusDataAction(MutexActionBase):
    '''
    Действие, которое запрашивает статусные данные семафора
    '''
    url = '/status-data'
    shortname = 'mutex.status-data'
    
    
    def run(self, request, context):
        '''
        '''
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        # 0. проверяем, что семафор должен находиться в состоянии "Занят не нами"
        _, mutex = m3_mutex.request_mutex(mutex_id)
        
        return actions.TextResult(unicode(mutex.status_data))
    
    
class ReleaseMutexOkAction(MutexActionBase):
    '''
    Действие на освобождение семафора
    '''
    
    url = '/release-ok'
    shortname = 'mutex.release-ok'
    
    def run(self, request, context):
        
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        m3_mutex.release_mutex(mutex_id)
                
        return actions.TextResult('ok') 
    
class ReleaseMutexFailAction(MutexActionBase):
    '''
    Действие на освобождение семафора
    '''
    
    url = '/release-fail'
    shortname = 'mutex.release-fail'
    
    def run(self, request, context):
        
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        try:
            m3_mutex.release_mutex(mutex_id)
        except m3_mutex.MutexBusy:
            return actions.TextResult('ok') 
                
        return actions.TextResult('fail')
    
class ShortCaptureMutexAction(MutexActionBase):
    '''
    Действие, которое выполняет захват семафора с очень которотким таймаутом
    '''
    
    url = '/capture-short'
    shortname = 'mutex.capture-short'

    def run(self, request, context):
        ''' 
        ''' 
        mutex_id = m3_mutex.MutexID(group=context.mutex_group, 
                                    mode=context.mutex_mode,
                                    id=context.mutex_id)
        
        m3_mutex.capture_mutex(mutex_id, auto_release=m3_mutex.TimeoutAutoRelease(timeout=2))
        
        return actions.TextResult('ok')