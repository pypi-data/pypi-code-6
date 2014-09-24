#coding:utf-8
'''
Created on 06.11.2010

@author: akvarats
'''

from django.db import models
from m3.data.mie import SimpleModelExtender, DatedModelExtender

class MainModel(models.Model):
    '''
    Основная модель, которую мы будем расширять с помощью механизма MIE
    '''
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    
    
class MainModelSimpleExtender1(SimpleModelExtender):
    
    main_model = models.ForeignKey(MainModel)
    info = models.TextField()
    
    class MieMeta:
        primary_model = MainModel
        primary_field = 'main_model'

class MainModelSimpleExtender2(SimpleModelExtender):
    
    mie_primary = models.ForeignKey(MainModel)
    info = models.TextField()
    dop_info = models.TextField()
    
    class MieMeta:
        primary_model = MainModel
        
class MainModelDatedExtender1(DatedModelExtender):
    
    mie_primary = models.ForeignKey(MainModel)
    date = models.DateField()
    info = models.TextField()
    
    class MieMeta:
        primary_model = MainModel
        date_field = 'date'