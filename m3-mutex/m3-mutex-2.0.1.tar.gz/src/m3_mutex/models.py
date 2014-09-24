#coding:utf-8
'''
Created on 18.07.2011

@author: akvarats
'''

from django.db import models


class MutexModel(models.Model):
    '''
    Модель хранения информации о семафоре
    '''

    # информация о семафоре
    mutex_group = models.CharField(max_length=100, blank=True)
    mutex_mode = models.CharField(max_length=100, blank=True)
    mutex_id = models.CharField(max_length=100)

    # информация о владельце семафора
    owner_session = models.CharField(max_length=50)
    owner_host = models.TextField(blank=True)
    owner_id = models.CharField(max_length=40, default='system')
    owner_login = models.CharField(max_length=40, blank=True)
    owner_name = models.CharField(max_length=100, blank=True)

    # условие автоосвобождения
    auto_release_rule = models.CharField(max_length=100, blank=True)
    auto_release_config = models.CharField(max_length=300, blank=True)

    # служебная информация
    captured_since = models.DateTimeField()

    # статусная информация
    status_data = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'm3_mutex'
