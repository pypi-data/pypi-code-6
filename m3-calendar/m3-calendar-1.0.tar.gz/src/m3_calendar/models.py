#coding:utf-8
'''
Created on 31.03.2011

@author: akvarats
'''

from django.db import models

from m3.db import BaseEnumerate

class ExceptedDayTypeEnum(BaseEnumerate):
    '''
    Тип дня, исключаемого из обычного календаря
    '''
    DAYOFF = 1
    HOLIDAY = 2
    WORKDAY = 3
    
    values = {DAYOFF: u'Выходной день',
              HOLIDAY: u'Праздничный день',
              WORKDAY: u'Рабочий день',}
    

class ExceptedDay(models.Model):
    '''
    Модель дня, исключенного из обычного календаря.
    '''
    name = models.CharField(max_length=200, null=True) # наименование выключенного дня
    day = models.DateField() # собственно, само значение даты
    type = models.SmallIntegerField(choices=ExceptedDayTypeEnum.get_choices()) # тип записи
    
