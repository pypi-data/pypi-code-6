#coding: utf-8
'''
Created on 10.06.2010

@author: akvarats
'''

from django.db import models
from django.contrib.auth.models import User

from metaroles import get_metarole


class UserRole(models.Model):
    '''
    Модель хранения роли пользователя в прикладной подсистеме
    '''
    # наименование роли пользователя
    name     = models.CharField(max_length = 200, db_index = True)
    
    # ассоциированная с ролью метароль (определяет интерфейс пользователя) 
    # может быть пустой
    metarole = models.CharField(max_length = 100, null = True, blank = True)
    
    def metarole_name(self):
        mr = get_metarole(self.metarole)
        return mr.name if mr else ''
    
    metarole_name.json_encode = True
    
    class Meta:
        db_table = 'm3_users_role'
        verbose_name = u'Роль пользователя'
        verbose_name_plural = u'Роли пользователя'
        
class RolePermission(models.Model):
    '''
    Разрешение, сопоставленное пользовательской роли. Кодирование и именование 
    разрешений будет выполняться следующим образом. У нас считается, что
    пользовательское разрешение кодируется в формате 
    ''' 
    role = models.ForeignKey(UserRole)
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
