# -*- coding: utf-8 -*-
from django.forms.formsets import ManagementForm

# --------------------------------------------------
# Классы, обслуживающие процесс миграции базы данных
# при выполнении обновлений прикладной и системный частей
# приложений
# --------------------------------------------------

from django.core import management

class MigrationManager:
    '''
    Класс, выполняющий проверку и дальнейшую миграцию базы данных
    '''
    def __init__(self):
        pass
    
    def migrate(self, applist):
        '''
        Выполняет миграцию приложений, указанных в applist
        '''
        for app in applist:
            management.call_command('migrate', app)