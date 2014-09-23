# -*- coding: utf-8 -*-
from djcelery.backends.database import DatabaseBackend


class AsyncTaskDatabaseBackend(DatabaseBackend):
    u"""
    Менеджер хранения состояний задач
    """
    # Экземпляр класса, реализующий уведомление о состоянии задач
    # должен иметь метод notify, принимающий модель задачи TaskModel
    notifier = None

    def _store_result(self, task_id, result, status, traceback=None, request=None):
        u"""
        Заменим стандартное поведение на собственное, чтобы обновлять
        дополнительные поля задачи из параметров запуска задачи
        request.kwargs['fields'] или из результата result['fields']
        """
        defaults = {}
        fields = {}
        # fields используются для обновления полей
        if result and isinstance(result, dict):
            fields = result.get('fields', {})
        # defaults используются только при создании новой записи
        if request:
            defaults = request.kwargs.get('fields', {})

        task = self.TaskModel._default_manager.store_result(
            task_id, result, status,
            traceback=traceback, children=self.current_task_children(request),
            defaults=defaults,
            **fields
        )
        self.notify(task, result, status, traceback, request)
        return result

    def notify(self, task, result, status, traceback=None, request=None):
        u"""
        Уведомление о состоянии задачи
        :param task: объект хранения состояния задачи (TaskModel)
        """
        if self.notifier is not None:
            self.notifier.notify(task)