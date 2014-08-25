from django.apps import AppConfig
from .task import tasks
from .broker import get_broker


class DistributedTaskConfig(AppConfig):
    name = 'distributed_task'
    verbose_name = "Distributed Task"

    def ready(self):
        tasks.discover()
        get_broker()