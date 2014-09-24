#coding:utf-8
'''
Created on 14.07.2011

@author: akvarats
'''

import datetime

from django.utils.translation import ugettext as _

class MutexID(object):
    '''
    Инкапсуляция над идентификатором экземпляра семафора
    '''
    def __init__(self, group='', mode='', id=''):
        self.group = group
        self.mode = mode
        self.id = id

class MutexOwner(object):
    '''
    Инкапсуляция над владельцем семафора
    '''
    def __init__(self, session_id='', user_id=0, name='', login='', host=''):
        self.session_id = session_id # идентификатор сессии, в рамках которой
        self.name = name # наименование (например, ФИО) владельца
        self.user_id = user_id # уникальный идентификатор владельца
        self.login = login # логин пользователя
        self.host = host # тачка, с которой был выставлен семафор
        
        # был установлен семафор
        
class SystemOwner(MutexOwner):
    '''
    Владелец, представленный в виде системного процесса
    '''    
    def __init__(self):
        super(SystemOwner, self).__init__(session_id='system',
                                          name='system', 
                                          login='',
                                          user_id=0, 
                                          host='server',)
        

class MutexState:
    '''
    Класс-перечисление возможных состояний семафора
    '''
    FREE = 1              # семафор свободен
    CAPTURED_BY_ME = 2    # семафор захвачен нами 
    CAPTURED_BY_OTHER = 3 # семафор захвачен другим
    
        
class Mutex(object):
    '''
    Класс семафора
    '''
    def __init__(self, id=MutexID(), owner=MutexOwner(), auto_release=None):
        self.id = id
        self.owner = owner
        self.auto_release = None
        self.captured_since = datetime.datetime.min
        self.status_data = None 
        
    def check_owner(self, owner):
        '''
        Возвращает True в случае, если указанный в параметрах owner совпадает
        с владельцем семафора
        '''
        return owner.session == self.session
    

class MutexAutoReleaseRule(object):
    '''
    Базовый класс, устанавливающий правила автоматического освобождения (снятия)
    семафора.
    
    Данный механизм необходим для того, чтобы семафоры не оставались в 
    системе "навсегда".
    '''
    
    def check(self, mutex):
        '''
        Основной метод, который возвращает True в случае, если 
        указанный данный семафор может быть освобожден в автоматическом
        режиме
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def dump(self):
        '''
        Возвращает кортеж из двух элементов для сохранения алгоритма
        автоматического освобождения семафоров в текстовом виде.
        
        Данный метод, будучи переопределенным в дочерних классах, должен вернуть
        кортеж из двух эелементов ('код правила', 'упакованные параметры срабатывания правила')
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def restore(self, config):
        '''
        Читает информацию о конфигурации условий автаматического освобождения
        семафоров из текстовой строки.
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    @staticmethod
    def get_rule_class(str='timeout'):
        
        if str == 'timeout':
            return TimeoutAutoRelease
        
        return None
    
class TimeoutAutoRelease(MutexAutoReleaseRule):
    '''
    Освобождение семафора на основании превышения времени ожидания.
    
    self.timeout указывается в целых секундах.
    '''
    
    DEFAULT_TIMEOUT = 300
    
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        
        self.timeout = timeout
    
    def check(self, mutex):
        '''
        Метод проверки на возможность получения 
        '''
        delta = datetime.datetime.now() - mutex.captured_since
        return delta.seconds > self.timeout if self.timeout else TimeoutAutoRelease.DEFAULT_TIMEOUT
    
    def dump(self):
        ''' 
        Возвращает информацию
        '''
        return ('timeout', str(self.timeout if self.timeout else TimeoutAutoRelease.DEFAULT_TIMEOUT),)
    
    def restore(self, config):
        '''
        '''
        try:
            self.timeout = int(config)
        except ValueError:
            self.timeout = TimeoutAutoRelease.DEFAULT_TIMEOUT
            
                
#===============================================================================
# Вспомогательные классы
#===============================================================================
class MutexQuery(object):
    '''
    Класс, представляющий запрос на получение 
    информации
    '''
    def __init__(self, filter='', start=0, offset=-1):
        self.filter = filter
        self.start = start
        self.offset = offset