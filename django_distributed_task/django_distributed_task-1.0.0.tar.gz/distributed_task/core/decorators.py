from ..task import tasks
from ..broker import get_broker


def register_task(cls):

    def delay(*args, **kwargs):
        broker = get_broker()

        module_path = tasks.get_task_path(cls)

        data = {
            'cmd': module_path,
            'args': args,
            'kwargs': kwargs
        }
        broker.produce_message(data)

    cls.delay = delay
    cls._is_registered_task = True

    return cls