#coding:utf-8

from datetime import timedelta
from django.db import models
from m3.db import BaseObjectModel, BaseEnumerate

class ExcTimedelta(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PeriodTypeEnum(BaseEnumerate):
    ONCE = 0
    HOURLY = 1
    DAILY = 2
    WEEKLY = 3
    
    values = {
        ONCE: u'Единожды',
        HOURLY: u'Ежечасно',
        DAILY: u'Ежедневно',
        WEEKLY: u'Еженедельно'
        }
    
    PERIOD_DELTAS = {
        HOURLY: timedelta(hours=1),
        DAILY: timedelta(1),
        WEEKLY: timedelta(7)
        }
        
def get_period_timedelta(period):        
    assert period in PeriodTypeEnum.PERIOD_DELTAS, 'Timedelta for period type %i is not set' \
        %period
    return PeriodTypeEnum.PERIOD_DELTAS[period]

class StatusTypeEnum(BaseEnumerate):
    NEW = 0
    OK = 1
    ERR = 2
    
    values = {
        NEW: u'Новое',
        OK: u'Выполнено успешно',
        ERR: u'Завершилось ошибкой',
    }

class Tasks(BaseObjectModel):
    task_name = models.CharField(max_length=200, db_index=True, blank=False)
    proc_name = models.CharField(max_length=200, null=False, blank=False)
    last_run = models.DateTimeField(null=True)
    next_run = models.DateTimeField()
    period = models.PositiveIntegerField(choices=PeriodTypeEnum.get_choices(),
                                            null=False, blank=False)
    executing = models.BooleanField(null=False, default=False)
    enabled = models.BooleanField(null=False, default=True)
    status = models.PositiveIntegerField(choices=StatusTypeEnum.get_choices(), 
                                 default=StatusTypeEnum.NEW,null=False, 
                                 blank=False)
    
    @property
    def period_name(self):
        return self.get_period_display()
    
    @property
    def status_name(self):
        return self.get_status_display()
    
    @property
    def is_new(self):
        return self.status == StatusTypeEnum.NEW

    class Meta:
        db_table = 'm3_task_scheduler'