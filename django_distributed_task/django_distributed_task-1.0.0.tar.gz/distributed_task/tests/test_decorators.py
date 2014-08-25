import unittest
import inspect

from distributed_task.core.decorators import register_task


def my_test_task():
    pass


class TaskDecoratorTest(unittest.TestCase):

    def test_decorator(self):
        new_method = register_task(my_test_task)

        assert inspect.isfunction(new_method.delay)