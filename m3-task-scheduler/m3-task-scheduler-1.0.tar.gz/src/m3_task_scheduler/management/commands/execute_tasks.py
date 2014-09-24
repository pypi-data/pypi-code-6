#coding:utf-8

from django.core.management.base import BaseCommand

from m3.contrib.m3_task_scheduler.api import execute_tasks

class Command(BaseCommand):
    def handle(self, *args, **options):
        execute_tasks()