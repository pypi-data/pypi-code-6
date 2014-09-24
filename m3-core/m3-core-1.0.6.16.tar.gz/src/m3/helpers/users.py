#coding:utf-8
'''
Created on 20.03.2010

@author: akvarats
'''
from django.http import HttpResponseRedirect

from m3.ui.actions.results import OperationResult

__all__ = ()

from django.db import models
from django.contrib.auth import models as django_auth_models

class BaseUserProfile(models.Model):
    '''
    Базовый класс для профилей пользователя прикладных
    приложений
    '''
    user = models.ForeignKey(django_auth_models.User, unique = True)
    class Meta:
        abstract = True
        

def authenticated_user_required(f):
    '''
    Декоратор проверки того, что к обращение к требуемому ресурсу системы
    производится аутентифицированным пользователем
    '''

    def action(request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated():
            if request.is_ajax():
                res = OperationResult.by_message(
                    u'Вы не авторизованы. Возможно, закончилось время пользовательской сессии.<br>'
                    u'Для повторной аутентификации обновите страницу.')
                return res.get_http_response()
            else:
                return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)

    return action