# -*- coding: utf-8 -*-
from djcelery.managers import TaskManager, transaction_retry, update_model_with_dict


class AsyncTaskManager(TaskManager):
    u"""
    Менеджер записи состояния задач
    """
    @transaction_retry(max_retries=2)
    def store_result(self, task_id, result, status,
                     traceback=None, children=None,
                     defaults=None, **kwargs):
        u"""
        Сохранение результатов и статуса задачи

        :param task_id: task id

        :param result: The return value of the task, or an exception
            instance raised by the task.

        :param status: Task status. See
            :meth:`celery.result.AsyncResult.get_status` for a list of
            possible status values.

        :keyword traceback: The traceback at the point of exception (if the
            task failed).

        :keyword children: List of serialized results of subtasks
            of this task.

        :keyword exception_retry_count: How many times to retry by
            transaction rollback on exception. This could theoretically
            happen in a race condition if another worker is trying to
            create the same task. The default is to retry twice.

        :param defaults: словарь полей для создания новой записи

        :param **kwargs: словарь полей для обновления существующей записи

        """
        default_params = {
             'status': status,
             'result': result,
             'traceback': traceback,
             'meta': {'children': children},
        }
        if status is None:
            del default_params['status']
        update_params = default_params.copy()
        update_params.update(kwargs)
        default_params.update(defaults)
        task, created = self.get_queryset().get_or_create(task_id=task_id, defaults=default_params)
        # если обновляем записи, то изменим параметры
        if not created:
            update_model_with_dict(task, update_params)
        return task
