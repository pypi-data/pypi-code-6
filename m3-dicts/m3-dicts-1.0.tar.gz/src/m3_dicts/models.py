#coding:utf-8

from django.db import models

from m3.db import BaseObjectModel


class DulType(BaseObjectModel):
    '''
    Модель документов, удостоверяющих личность
    '''
    code = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'm3_dicts_dultype'