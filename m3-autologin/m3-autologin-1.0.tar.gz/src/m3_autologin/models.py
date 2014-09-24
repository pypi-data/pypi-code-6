#coding:utf-8
'''
Created on 08.07.2011

@author: akvarats
'''

from django.db import models

from django.utils.translation import ugettext as _

from m3.db import BaseEnumerate
from m3_audit import AuditManager, BaseAuditModel



class AutoLoginTypeEnum(BaseEnumerate):
    '''
    Перечисление возможных типов автоматического входа в систему
    '''
    REMOTE_AUTH = 1
    NO_PASSWORD = 2
    
    values = {REMOTE_AUTH: _(u'Автовход с аутентификацией на удаленном сервере'),
              NO_PASSWORD: _(u'Автовход без указания пароля'),}
    
    verbose_map = {'remote-auth': REMOTE_AUTH,
                   'no-password': NO_PASSWORD,
                   }

class AutoLoginAudit(BaseAuditModel):
    '''
    Модель для хранения записей аудита автоматических входов в систему
    '''
    
    # тип автоматического входа в систему
    type = models.SmallIntegerField(choices=AutoLoginTypeEnum.get_choices(),
                                    default=AutoLoginTypeEnum.REMOTE_AUTH)
    
    # удаленный адрес, с которого был выполнен автовход
    remote_address = models.CharField(max_length=100, blank=True)
    
    
    @classmethod
    def write(cls, user, type='remote-password', request = None, *args, **kwargs):

        audit = cls()
        audit.by_user(user)
        
        audit.type = AutoLoginTypeEnum.verbose_map.get(type, 0)
        audit.remote_address = request.META.get('HTTP_X_FORWARDED_FOR', '') if request else ''
        
        audit.save()
        
    class Meta:
        db_table = 'm3_autologin_audit'
        
AuditManager().register('auto-login', AutoLoginAudit)


#===============================================================================
# Модель для хранения тикетов при удаленной авторизации
#===============================================================================
class RemoteAuthTicket(models.Model):
    '''
    Модель хранения тикета для удаленного входа пользователя
    '''
    # имя пользователя, для которого выдан тикет
    user_login = models.CharField(max_length=100)
    
    # идентификатор тикета (уникальное значение, которое гоняется
    # между данной системой и системой, в которой реализуется удаленная 
    # авторизация) 
    ticket_key = models.CharField(max_length=20)
    
    # содержимое тикета. здесь
    ticket_hash = models.CharField(max_length=100)
    
    # дата и время выдачи тикета
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'm3_autologin_tickets'