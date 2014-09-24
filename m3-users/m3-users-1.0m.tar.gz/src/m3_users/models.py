#coding: utf-8
'''
Created on 10.06.2010

@author: akvarats
'''

from django.db import models
from django.contrib.auth.models import User

from m3.db import BaseEnumerate
from m3.core.json import json_encode

from metaroles import get_metarole

class OrgTypes(BaseEnumerate):
    """ Тип организации """
    NULL = 0
    MO = 1
    SMO  = 2
    TFOMS = 3
    values = {
        NULL: u'нет привязки',
        MO: u'МО',
        SMO: u'СМО',
        TFOMS: u'Подразделение ТФОМС'}

class UserRole(models.Model):
    '''
    Модель хранения роли пользователя в прикладной подсистеме
    '''
    # наименование роли пользователя
    name     = models.CharField(max_length = 200, db_index = True)
    
    # ассоциированная с ролью метароль (определяет интерфейс пользователя)
    # может быть пустой
    metarole = models.CharField(max_length = 100, null = True, blank = True)

    org = models.PositiveSmallIntegerField(default=OrgTypes.NULL, choices=OrgTypes.get_choices())
    
    def metarole_name(self):
        mr = get_metarole(self.metarole)
        return mr.name if mr else ''

    metarole_name.json_encode = True

    @json_encode
    def org_type(self):
        """
        """
        return OrgTypes.values[self.org]
    
    class Meta:
        db_table = 'm3_users_role'
        verbose_name = u'Роль пользователя'
        verbose_name_plural = u'Роли пользователя'


class UserMetarole(models.Model):
    """
    Модель хранения сопоставления роли пользователя и метаролей.
    Появилась потому, что одной роли может соответствовать множество метаролей.
    """

    # Роль
    user_role = models.ForeignKey(UserRole)

    # ассоциированная с ролью метароль (определяет интерфейс пользователя)
    # может быть пустой
    metarole = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'm3_users_metarole'
        verbose_name = u'Метароль пользователя'
        verbose_name_plural = u'Метароли пользователя'

        
class RolePermission(models.Model):
    '''
    Разрешение, сопоставленное пользовательской роли. Кодирование и именование 
    разрешений будет выполняться следующим образом. У нас считается, что
    пользовательское разрешение кодируется в формате 
    '''
#    role = models.ForeignKey(UserRole)

    user_metarole = models.ForeignKey(UserMetarole, null=True)
    # здесь указывается код разрешения в формате 'модуль1.подмодуль.подмодуль.подмодуль...код разрешения'
    permission_code = models.CharField(max_length=200, db_index = True)
    
    # человеческое наименование разрешения с наименованиями модулей, разделенных
    # через запятые
    verbose_permission_name = models.TextField()
    
    disabled = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'm3_users_rolepermissions'

    
class AssignedRole(models.Model):
    '''
    Роль, назначенная на пользователя
    '''
    user = models.ForeignKey(User, related_name='assigned_roles')
    role = models.ForeignKey(UserRole, related_name='assigned_users')
    
    def user_login(self):
        return self.user.username if self.user else ''
    
    def user_first_name(self):
        return self.user.first_name if self.user else ''
    
    def user_last_name(self):
        return self.user.last_name if self.user else ''
    
    def user_email(self):
        return self.user.email if self.user else ''
    
    user_login.json_encode = True
    user_first_name.json_encode = True
    user_last_name.json_encode = True
    user_email.json_encode = True
    
    class Meta:
        db_table = 'm3_users_assignedrole'
