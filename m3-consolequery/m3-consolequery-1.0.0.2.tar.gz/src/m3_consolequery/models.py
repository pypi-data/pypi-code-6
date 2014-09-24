#coding:utf-8
'''
Модуль содержит общие модели справочников и перечисления для всех подсистем МИС.
'''
from django.db import models

#===============================================================================
# Справочник запросов
#===============================================================================

class CustomQueries(models.Model):
    '''
    Справочник "Пользовательские запросы"
    '''
    code = models.CharField(max_length = 20, db_index=True, null=True, blank=True)
    name = models.CharField(max_length = 200, db_index=True)
    query = models.TextField()
    
    class Meta:
        db_table = 'm3_conquery_customqueries'
