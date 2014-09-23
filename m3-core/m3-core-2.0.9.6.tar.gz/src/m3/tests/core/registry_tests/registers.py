#coding:utf-8
'''
Регистры, которые учавствуют в тестах

Created on 12.04.2011

@author: akvarats
'''

from m3.core.registry import CumulativeRegister, PeriodEnum

from models import RegisterDayModel, OperdateRegisterModel

class CumulativeDayRegister(CumulativeRegister):
    '''
    Простой куммулятивный регистр
    '''
    model = RegisterDayModel
    
    dim_fields = ['dim1', 'dim2', 'dim3',]
    rest_fields = ['rest1', 'rest2',]
    circ_fields = ['circ1', 'circ2',]
    
    date_field = 'date'
    
    
class OperdateRegister(CumulativeRegister):
    '''
    Регистр для тестов случаев, когда поле хранения системной
    даты регистра называется не date.
    '''
    model = OperdateRegisterModel
    date_field = 'operdate'
    dim_fields = ['dim',]
    rest_fields = ['balance',]
    circ_fields = ['oborot',]