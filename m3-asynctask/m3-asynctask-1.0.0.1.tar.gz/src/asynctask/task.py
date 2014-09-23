# -*- coding: utf-8 -*-
from celery import Task, task, states
from kombu import uuid


class AsyncTask(Task):
    u"""
    Задача, сохраняемая при асинхронном запуске
    """
    abstract = True
    track_started = True

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, **options):
        u"""
        Сохраним состояние задачи перед асинхронным запуском
        """
        task_id = task_id or uuid()
        # передадим атрибут fields из описания задачи в ее параметры
        if hasattr(self, 'fields') and isinstance(self.fields, dict):
            fields = self.fields.copy()
            fields.update(kwargs.get('fields', {}))
            kwargs['fields'] = fields
        self.request.kwargs = kwargs
        self.update_state(task_id=task_id, state=states.PENDING)
        return super(AsyncTask, self).apply_async(args, kwargs, task_id, producer, link, link_error, **options)

    def update_state(self, task_id=None, state=None, meta=None):
        if task_id is None:
            task_id = self.request.id
        self.backend.store_result(task_id, meta, state, request=self.request)


def async_task(*args, **kwargs):
    u"""
    Декоратор для задачи AsyncTask
    """
    params = {
        'base': AsyncTask,
    }
    params.update(kwargs)
    return task(*args, **params)