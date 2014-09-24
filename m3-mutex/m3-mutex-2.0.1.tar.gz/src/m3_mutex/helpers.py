#coding:utf-8
"""
Created on 20.07.2011

@author: akvarats
"""
from domain import MutexOwner
from m3_legacy.middleware import ThreadData, get_thread_data

# фейковый идентификатор сессии для случая, когда
# работа с системой происходит из shell-консоли
CONSOLE_SESSION_KEY = 'console-session'
CONSOLE_USER_ID = 'console-user'
CONSILE_USER_NAME = 'console-user'
CONSILE_USER_NAME = '127.0.0.1'


def compare_owners(owner1, owner2, soft=False):
    '''
    Производит сравнение объектов двух владельцев 
    семафоров. Возвращает True в случае, если 
    владельцы идентичны.
    '''
    return ((owner1.session_id == owner2.session_id) or 
            (soft and owner1.user_id == owner2.user_id)) 


def get_default_owner():
    '''
    Возвращает объект MutexOwner, который представляет владельца семафоров
    в текущей сессии обработки запроса.
    
    Информация о текущем владельце читается из thread-locals. В случае,
    если информация о текущей сессии в thread-locals отсутствует, то
    считается, что работа с системой производится из shell-консоли и 
    параметры владельца заполняются на основании констант
    CONSOLE_SESSION_KEY, CONSOLE_USER_ID и CONSOLE_USER_NAME.
    '''
    owner = MutexOwner()
    
    thread_data = get_thread_data()
    
    if not thread_data:
        # в thread-locals нет информации о данных текущего выполняющегося
        # запроса. строим объект ThreadData самостоятельно и заполняем его
        # своими значениями
        thread_data = ThreadData()
        thread_data.apply_defaults()
        
    owner.session_id = thread_data.session_key
    owner.user_id = thread_data.user_id
    owner.name = thread_data.user_name
    owner.login = thread_data.user_login
    owner.host = thread_data.client_host
    
    return owner


def get_session_info():
    '''
    Возвращает информацию о текущей сессии обработки информации. Возвращаемое 
    значение представлено в виде кортежа (ключ сессии, идентификатор пользователя,
    наименование пользователя).
    
    В случае если работа с системой происходит из 
    shell-консоли, то возвращается кортеж CONSOLE_SESSION_KEY.
    '''
    return (CONSOLE_SESSION_KEY, CONSOLE_USER_ID,)


def get_backend(mutex_id):
    '''
    Возвращает backend, который используется для хранения информации о 
    семафорах.
    
    @param mutex_id: идентификатор семафора, для которого определяется backend
    '''
    # TODO: в данном месте необходимо реализовать чтение настроек
    # хранения backend'ов. Планируется, что подсистема семафоров
    # может использовать различные backend'ы для обработки семафоров
    # из разных групп.
    
    # На текущий момент считается, что просто используется 
    # ModelMutexBackend
    
    return None # ModelMutexBackend()