#coding:utf-8
'''
Created on 08.07.2011

@author: akvarats
'''

from django.conf import settings

AUTOLOGIN_SETTINGS_NAME = 'M3_AUTOLOGIN_CONF'
AUTOLOGIN_ALLOW_REMOTE_AUTH = 'M3_AUTOLOGIN_ALLOW_REMOTE_AUTH'

def read_autologin_config(conf, autologin_section_name='auto-login', default_url = '/'):
    '''
    Метод читает настройки автоматического логина из
    conf-файла приложения.
    
    Вызов данной процедуры необходимо вставить в settings.py
    прикладного приложения следующим образом
    
    M3_AUTOLOGIN_CONF = read_autologin_config(conf), где
    conf - экземпляр стандартный экземпляр m3.helpers.config.ProjectConfig
    '''
    result = {}
    
    autologin_items = conf.items(autologin_section_name)
    for item in autologin_items:
        if len(item) < 2:
            continue
        
        separated_value = item[1].split(',')
        result[item[0]] = (separated_value[0].strip(), 
                           (separated_value[1] if len(separated_value) > 1 and separated_value[1].strip() else default_url).strip())
            
            
    return result


def get_autologin_config():
    '''
    Возвращает настройку автовхода в систему.
    '''
    return getattr(settings, AUTOLOGIN_SETTINGS_NAME, {})


def allow_remote_auth():
    '''
    Функция, возвращающая True в случае, если в системе разрешен
    удаленный метод аутентификации пользователей.
    
    По умолчанию такое поведение является запрещенным.
    '''
    return getattr(settings, AUTOLOGIN_ALLOW_REMOTE_AUTH, False)