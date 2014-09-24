#coding:utf-8
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.management import call_command

import api as task_api
from models import Tasks, PeriodTypeEnum, StatusTypeEnum


class TestTaskSchedule(TestCase):
    
    def test_1(self):
        # Регистрация задачи
        task_api.register_task(
            task_name = 'tst', 
            proc = simpel_proc, 
            next_run = datetime.now(), 
            period = PeriodTypeEnum.WEEKLY)
        
        # Проверка существование задачи
        Tasks.objects.get(task_name='tst')
        
        # Проверка запуска через команду
        call_command('execute_tasks')
        task = Tasks.objects.get(task_name='tst')
        self.assertTrue(task.next_run > datetime.now() + timedelta(6))
        self.assertFalse(task.executing)
        self.assertEqual(task.status, StatusTypeEnum.OK)
        
        # Удаление задачи
        task_api.remove_task('tst')
        self.assertFalse(Tasks.objects.filter(task_name='tst').exists())

def simpel_proc():
    return 'test msg'