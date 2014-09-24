#coding:utf-8
'''
Created on 16.08.2011

@author: akvarats
'''

from django.utils.translation import ugettext as _

from m3.db import BaseEnumerate

class ServerUrls(object):
    '''
    Перечисление урлов, которые используются при отсылке запросов с клиента в транспортный сервер.
    '''
    
    FORWARD_MESSAGE = 'message/forward'
    PING = 'ping'
    ECHO = 'echo'
    
    

class ClientUrls(object):
    '''
    Перечисление урлов, которые используются при отсылке запросов с транспортного сервера (интеграционной шины)
    клиентам.
    '''
    pass


class InteractionMode(BaseEnumerate):
    '''
    Перечисление режимов взаимодействий, в которые вступают клиент и транспортный сервер
    '''
    SYNC = 1
    ASYNC = 2
    
    values = { SYNC: _(u'Синхронный режим'),
               ASYNC: _(u'Асинхронный режим'),}
    
    names = { SYNC: 'SYNC',
              ASYNC: 'ASYNC', }
    
    reversed_names = { 'SYNC': SYNC,
                       'ASYNC': ASYNC, }

PING_SUCCESSFUL_REQUEST = 'pong'