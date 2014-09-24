#coding:utf-8
'''
Created on 08.07.2011

@author: akvarats
'''

import uuid
import datetime 

from django.http import (HttpResponse, 
                         HttpResponseRedirect, 
                         HttpResponseForbidden,
                         HttpResponseNotFound,)


from django.contrib.auth import login, logout, get_backends
from django.contrib.auth.models import User, get_hexdigest

from m3_audit import AuditManager


from m3.helpers import logger

from api import (get_autologin_config, allow_remote_auth,)
from models import RemoteAuthTicket


URL_REDIRECT_ON_ERROR = '/'

def autologin_view(request, login_option):
    '''
    Обработчик автоматического входа в систему в систему с 
    '''
    
    autologin_config = get_autologin_config()
     
    username, url = autologin_config.get(login_option, [None,None])
    
    if not username:
        # пока вот так, редиректим просто на главную страницу
        logger.error(u'Не указано имя пользователя для варианта автоматического входа в систему %s.' % login_option)
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        logger.error(u'Пользователя с именем %s не существует для варианта автоматического входа в систему %s.' % (username, login_option))
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    if not user.is_active:
        logger.error(u'Пользователя с именем %s заблокирован и не может быть использован для варианта автоматического входа в систему %s.' % (username, login_option))
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    auth_backends = get_backends()
    if auth_backends:
        user.backend = "%s.%s" % (auth_backends[0].__module__, 
                                  auth_backends[0].__class__.__name__)
    
    logout(request)
    login(request, user)
    
    # пишем запись в аудит входа
    AuditManager().write('auth', user=user)
    AuditManager().write('auto-login', user=user, type='no-password', request=request)
    
    
    return HttpResponseRedirect(url)


def ticket_view(request):
    '''
    Представление для получения тикета на выполнение удаленной аутентификации
    пользователя.
    
    В случае если операция удаленной аутентификации с использованием
    тикетов запрещена, то возвращается response со статус кодом 403.
    
    В случае, если пользователь не найден или является неактивным, то возвращается 
    response со статус кодом 404.
    
    В случае успешного выполнения операции оформления тикета возвращается
    response со статус кодом 200.
    '''
    if not allow_remote_auth():
        # наверное, нужна специальная страница на forbidden..
        return HttpResponseForbidden()
    
    username = request.REQUEST.get('username', '')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    
    if not user.is_active:
        return HttpResponseNotFound()
    
    algo, salt, hash = user.password.split('$')
    
    ticket = RemoteAuthTicket()
    ticket.user_login = username
    ticket.ticket_key = str(uuid.uuid4())[0:8]
    ticket.ticket_hash = get_hexdigest(algo, ticket.ticket_key, hash)
    
    ticket.save()
    
    return HttpResponse('%s$%s$%s' % (algo, salt, ticket.ticket_key))
    
    
def remote_login_view(request):
    '''
    Представление, обрабатывающее запрос на удаленную аутентификацию пользователя.
    
    В случае если операция удаленной аутентификации запрещена, то выдается 
    response со статус кодом 403.
    
    В случае если указанный в запросе ключ
    '''
    
    if not allow_remote_auth():
        # возвращаем статус код, соответствующий недопустимому запросу на сервер
        return HttpResponseForbidden()
    
    ticket_key = request.REQUEST.get('ticket_key', '!')
    ticket_hash = request.REQUEST.get('hash', '!')
    
    try:
        ticket = RemoteAuthTicket.objects.get(ticket_key=ticket_key)
    except RemoteAuthTicket.DoesNotExist:
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    if ticket.ticket_hash != ticket_hash:
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    try:
        user = User.objects.get(username=ticket.user_login)
    except User.DoesNotExist:
        return HttpResponseRedirect(URL_REDIRECT_ON_ERROR)
    
    # чистим тикеты
    # 1. удаляем текущий тикет
    ticket.delete()
    # 2. удаляем тикеты, которым больше 1 часа
    RemoteAuthTicket.objects.filter(created__lte=datetime.datetime.now() - datetime.timedelta(hours=1)).delete()
     
    # всё ок, выполняем вход в систему
    auth_backends = get_backends()
    if auth_backends:
        user.backend = "%s.%s" % (auth_backends[0].__module__, 
                                  auth_backends[0].__class__.__name__)
    
    logout(request)
    login(request, user)
    
    # пишем запись в аудит входа
    AuditManager().write('auth', user=user)
    AuditManager().write('auto-login', user=user, type='remote-auth', request=request)
    
    
    # тут пока жесткий URL, необходимо бы сделать так, чтобы редиректить на
    # URL, задаваемый извне
    return HttpResponseRedirect('/')