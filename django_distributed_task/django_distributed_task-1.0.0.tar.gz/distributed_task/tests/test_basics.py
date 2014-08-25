import unittest


class BasicTest(unittest.TestCase):

    def test_task_registry(self):
        from distributed_task import task
        from distributed_task.task.registry import TaskRegistry

        self.assertIsInstance(task.tasks, TaskRegistry, "Task registry is not available")