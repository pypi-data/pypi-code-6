#coding:utf-8
'''
Created on 12.04.2011

@author: akvarats
'''

from django.db import models

class RegisterDayModel(models.Model):
    '''
    Модель хранения записей регистра
    '''
    date = models.DateField()
    
    # измерения
    dim1 = models.CharField(max_length=100)
    dim2 = models.IntegerField()
    dim3 = models.CharField(max_length=30)
    
    # ресурсы накопления
    rest1 = models.DecimalField(max_digits=16, decimal_places=4)
    rest2 = models.DecimalField(max_digits=16, decimal_places=4)
    
    # ресурсы оборотов
    circ1 = models.DecimalField(max_digits=16, decimal_places=4)
    circ2 = models.DecimalField(max_digits=16, decimal_places=4)    
    
    
class OperdateRegisterModel(models.Model):
    '''
    Модель хранения данных регистра, в котором для хранения системной даты
    используется поле с названием, отличным от date
    '''
    operdate = models.DateField(db_index=True)
    
    dim = models.CharField(max_length=10, db_index=True)
    
    balance = models.DecimalField(max_digits=16, decimal_places=2)
    oborot = models.DecimalField(max_digits=16, decimal_places=2)