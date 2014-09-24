#coding:utf-8
'''
Created on 12.04.2011

@author: akvarats
'''
import calendar
from datetime import datetime

class PeriodEnum:
    
    INFTY = 1 # в регистре нет периодичности и нет динамически хранящихся
    SECOND = 2 # до секунд
    MINUTE = 3
    HOUR = 4
    DAY = 5
    MONTH = 6
    QUARTER = 7
    YEAR = 8

def normdate(period, date, begin = True):
    '''
    Метод нормализует дату в зависимости от периода
    @ begin = True - даты выравниваются на начало, иначе на конец
    '''
    if not date:
        return None        
    if period == PeriodEnum.SECOND:
        return datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
    if period == PeriodEnum.MINUTE:
        return datetime(date.year, date.month, date.day, date.hour, date.minute, 0 if begin else 59)
    if period == PeriodEnum.HOUR:
        return datetime(date.year, date.month, date.day, date.hour, 0 if begin else 59, 0 if begin else 59)
    if period == PeriodEnum.DAY:
        return datetime(date.year, date.month, date.day, 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PeriodEnum.MONTH:
        return datetime(date.year, date.month, 1 if begin else calendar.monthrange(date.year, date.month)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PeriodEnum.QUARTER:
        if date.month < 4:
            return datetime(date.year, 1 if begin else 3, 1 if begin else calendar.monthrange(date.year, 1 if begin else 3)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        if date.month < 7:
            return datetime(date.year, 4 if begin else 6, 1 if begin else calendar.monthrange(date.year, 4 if begin else 6)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        if date.month < 10:
            return datetime(date.year, 7 if begin else 9, 1 if begin else calendar.monthrange(date.year, 7 if begin else 9)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        return datetime(date.year, 10 if begin else 12, 1 if begin else calendar.monthrange(date.year, 10 if begin else 12)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PeriodEnum.YEAR:
        return datetime(date.year, 1 if begin else 12, 1 if begin else calendar.monthrange(date.year, 1 if begin else 12)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    return date