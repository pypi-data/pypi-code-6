# -*- coding: utf-8 -*-

from .occult._generator.configreader import ConfigReader

from .occult._generator.task import CongfigureTask
from .occult._generator.task import CopyTask
from .occult._generator.task import RenderTask

class TaskManager(object):
    def __init__(self, path=None, extra=None):
        self.path = path
        self.extra = extra if extra is not None else {}
        self.data = ConfigReader(self.path)
        self.tasks = []
        self.out = {}

        tasks = self.data.get('tasks', None)

        if len(tasks):
            for task in tasks:
                self.add_task(task)

    def add_task(self, task=None):
        t = None
        if task.get('command') == 'configure':
            t = CongfigureTask(task)
        elif task.get('command') == 'copy':
            t = CopyTask(task)
        elif task.get('command') == 'render':
            t = RenderTask(task)

        if t is not None:
            t.taskmanager = self;
            self.tasks.append(t)

    def run_all(self):
        for index,task in enumerate(self.tasks):
            if index+1<=len(self.tasks)-1:
                task.nextTask = self.tasks[index+1]

        if len(self.tasks) > 0:
            self.tasks[0].do_actions()
