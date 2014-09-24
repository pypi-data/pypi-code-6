#coding:utf-8

from datetime import datetime

from django.utils.importlib import import_module

from m3.helpers import logger

from models import (Tasks, get_period_timedelta, 
                    StatusTypeEnum as stats, 
                    PeriodTypeEnum as periods)

class TaskExists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
def execute_tasks():
    '''
    Выполнение задач.
    '''
    tasks_ran = 0
    tasks_err = 0
    tasks = Tasks.objects.filter(next_run__lte=datetime.now(), 
                                 executing=False, enabled=True)
    for task in list(tasks): 
        task.executing = True
        task.last_run = datetime.now()
        task.save()
        tasks_ran += 1
        try:
            proc = get_proc(task.proc_name)
            if task.period != periods.ONCE:
                timedelta = get_period_timedelta(task.period)
            proc()
        except Exception as e:
            task.status = stats.ERR
            tasks_err += 1
            logger.exception(str(e))
            print str(e)
        else:
            task.status = stats.OK
            if task.period == periods.ONCE:
                task.enabled = False
            else:
                task.next_run += timedelta
        task.executing = False
        task.last_run = datetime.now()
        task.save()
    report_msg = u'Выполнено задач всего: %i. \nИз них завершено с ошибками: %i.' \
                 %(tasks_ran,tasks_err)
    print report_msg
    logger.info(report_msg)
            
    
def register_task(task_name, proc,
                  next_run=datetime.now(), 
                  period=periods.DAILY):
    '''
    Внесение задачи в расписание.
    '''
    assert task_name,'Empty task_name not allowed.'
    assert proc,'Empty procedures are not allowed.'
    assert callable(proc), 'Procedure %s.%s is not callable.' \
        %(proc.__module__,proc.__name__)
    if Tasks.objects.filter(task_name=task_name).exists():
        raise TaskExists('Task %s already exists.' %task_name)
    if period != periods.ONCE:
        get_period_timedelta(period)
    task = Tasks(task_name=task_name,
                 proc_name=proc.__module__+'.'+proc.__name__, 
                 next_run=next_run,
                 period=period)
    task.save()
    return task

def remove_task(task_name):
    '''
    Удаление задачи из расписания.
    '''
    try:
        task = Tasks.objects.get(task_name=task_name)
    except Tasks.DoesNotExist:
        return False
    else:
        task.delete()
        return True
    
def get_proc(proc_name):
    '''
    Извлекает процедуру по названиям модуля и процедуры.
    '''
    module_name, _, proc_name_short = proc_name.rpartition('.')
    module = import_module(module_name)
    proc = getattr(module, proc_name_short, None)
    assert callable(proc), 'Procedure %s is not callable.' \
        %(proc_name)
    return proc