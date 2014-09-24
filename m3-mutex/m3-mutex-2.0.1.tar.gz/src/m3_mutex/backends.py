#coding:utf-8
'''
Created on 15.07.2011

@author: akvarats
'''

import datetime

from django.utils.translation import ugettext as _
from django.db.models import F

from domain import (Mutex, MutexState, MutexID, MutexOwner, MutexAutoReleaseRule, 
                    TimeoutAutoRelease)
                     
from models import MutexModel
from helpers import compare_owners, get_default_owner
from exceptions import MutexBusy

class BaseMutexBackend(object):
    '''
    Базовый класс (интерфейс) бекэнда для управления семафорами.
    '''
    
    def capture_mutex(self, mutex_id, owner=None, auto_release=TimeoutAutoRelease(), status_data=None):
        '''
        Метод захвата семафора.
        
        @param mutex_id: либо объект класса domain.Mutex, либо domain.MutexID
        @param owner: объект класса domain.MutexOwner, который представляет 
            владельца семафора. Если передать значение None, то будет
            использованы значения из thread-locals
        @param auto_release: правило автоосвобождения данного семаформа. По 
            умолчанию используется автоматическое освобождение по таймауту
            в 5 минут.
        '''
        
        if not owner:  
            owner = get_default_owner()
        
        cleaned_status_data = ''
        
        if status_data != None:
            if hasattr(status_data, 'dump') and callable(status_data.dump):
                cleaned_status_data = status_data.dump()
            else:
                cleaned_status_data = unicode(status_data)
         
        mutex = self._read_mutex(mutex_id)
        
        create_mutex = False # признак того, что необходимо создать новый семафор
        if mutex:
            # проверяем условие автоосвобождения семафора
            if mutex.auto_release and mutex.auto_release.check(mutex):
                self._remove_mutex(mutex_id)
                create_mutex = True
            else:
                if not compare_owners(mutex.owner, owner):
                    raise MutexBusy()
                # семафор был ранее захвачен нами, обновляем информацию
                # об его захвате
                self._refresh_mutex(mutex_id, cleaned_status_data)
        else:
            create_mutex = True
            
        if create_mutex:
            mutex = Mutex()
            mutex.id = mutex_id
            mutex.owner = owner
            mutex.captured_since = datetime.datetime.now()
            mutex.auto_release = auto_release
            mutex.status_data = cleaned_status_data 
            
            self._add_mutex(mutex)
            
        return mutex
        
    
    def release_mutex(self, mutex_id, owner=None):
        '''
        Метод освобождения семафора.
        
        В случае, если семафор был ранее захвачен не нами  
        '''
        mutex = self._read_mutex(mutex_id)
        if not mutex:
            return
        
        if not owner:
            owner = get_default_owner()
            
        if not compare_owners(mutex.owner, owner):
            raise MutexBusy()
        
        self._remove_mutex(mutex_id)
        
    
    def request_mutex(self, mutex_id, owner=None):
        '''
        Метод проверки состояния семафора. 
        
        Возвращает значение перечисления кортеж из двух элементов.
        Первым элементом указывается состояние семафора (mutex.) 
        '''
        mutex = self._read_mutex(mutex_id)
        
        if not mutex:
            return (MutexState.FREE, None)
        
        if mutex.auto_release and mutex.auto_release.check(mutex):
            self._remove_mutex(mutex_id)
            return (MutexState.FREE, None)
        
        if not owner:
            owner = get_default_owner()
        
        return (MutexState.CAPTURED_BY_ME if compare_owners(mutex.owner, owner) else MutexState.CAPTURED_BY_OTHER, mutex) 
        
    
    #===========================================================================
    # Методы, которые должны быть переопределены в классах конкретных
    # backend'ов
    #===========================================================================
    def _read_mutex(self, mutex_id):
        '''
        Внутренний метод чтения информации о семафоре из хранилища
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def _add_mutex(self, mutex):
        '''
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def _refresh_mutex(self, mutex_id, status_data):
        '''
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def _remove_mutex(self, mutex_id):
        '''
        @param mutex: объект класса domain.Mutex, который необходимо
        удалить из хранилища семафоров. 
        '''
        raise NotImplementedError(_(u'Данный метод должен быть переопределен в классах-потомках'))
        
    
class ModelMutexBackend(BaseMutexBackend):
    '''
    Бекэнд, который реализует хранение семафоров в базе данных
    '''
    
    def _read_mutex(self, mutex_id):
        '''
        Читаем параметры семафора из базы данных
        '''
        try:
            stored_mutex = MutexModel.objects.get(mutex_group=mutex_id.group,
                                                  mutex_mode=mutex_id.mode,
                                                  mutex_id=mutex_id.id)
            mutex = Mutex()
            mutex.id.group = stored_mutex.mutex_group
            mutex.id.mode = stored_mutex.mutex_mode
            mutex.id.id = stored_mutex.mutex_id
            
            mutex.owner.session_id = stored_mutex.owner_session
            mutex.owner.host = stored_mutex.owner_session
            mutex.owner.user_id = stored_mutex.owner_id 
            mutex.owner.login = stored_mutex.owner_login
            mutex.owner.name = stored_mutex.owner_name
            
            mutex.captured_since = stored_mutex.captured_since
            mutex.status_data = stored_mutex.status_data
            
            # восстановление правила автоосвобождения семафора
            auto_release_class = MutexAutoReleaseRule.get_rule_class(stored_mutex.auto_release_rule)
            if auto_release_class:
                mutex.auto_release = auto_release_class()
                mutex.auto_release.restore(stored_mutex.auto_release_config)
            
        except MutexModel.DoesNotExist:
            mutex = None
        
        return mutex
    
    def _add_mutex(self, mutex):
        '''
        Записывает информацию о захвате семафора в базу данных.
        '''
        mutex_model = MutexModel()
        
        mutex_model.mutex_group = mutex.id.group 
        mutex_model.mutex_mode = mutex.id.mode 
        mutex_model.mutex_id = mutex.id.id
        
        mutex_model.owner_session = mutex.owner.session_id 
        mutex_model.owner_host = mutex.owner.host
        mutex_model.owner_id = mutex.owner.user_id
        mutex_model.owner_login = mutex.owner.login
        mutex_model.owner_name = mutex.owner.name
        
        mutex_model.captured_since = mutex.captured_since 
        mutex_model.status_data = mutex.status_data
        
        if mutex.auto_release:
            auto_release_tuple = mutex.auto_release.dump()
            mutex_model.auto_release_rule = auto_release_tuple[0]
            mutex_model.auto_release_config = auto_release_tuple[1]
        
        mutex_model.save()
        
    
    def _refresh_mutex(self, mutex_id, status_data=''):
        '''
        Производит обновление информации об установке семафора. Выставляет
        текущую дату в качестве метки момента захвата семафора.
        '''
        MutexModel.objects.filter(mutex_group=mutex_id.group,
                                  mutex_mode=mutex_id.mode,
                                  mutex_id=mutex_id.id).update(captured_since=datetime.datetime.now(),
                                                               status_data=status_data or F('status_data'))
                                  
    def _remove_mutex(self, mutex_id):
        '''
        Удаляет информацию о захвате семафора из базы данных
        '''
        MutexModel.objects.filter(mutex_group=mutex_id.group,
                                  mutex_mode=mutex_id.mode,
                                  mutex_id=mutex_id.id).delete()

class SessionMutexBackend(BaseMutexBackend):
    '''
    Бекэнд, который реализует хранение семафоров в сессии
    текущей обработки запросов.
    
    Данный бекэнд необходимо использовать для выставления семафоров
    только в рамках обработки текущего запроса.
    '''
    pass 
