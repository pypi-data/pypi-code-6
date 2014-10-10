from unittest import TestCase

from vecnet.simulation import ExecutionRequest


class ExecutionRequestTests(TestCase):
    """
    Tests for the ExecutionRequest class.
    """

    def test_from_dict(self):
        d = {
            'simulation_group': None,
            'input_files': None,
        }
        execution_request = ExecutionRequest.from_dict(d)
        self.assertIsNone(execution_request.simulation_group)
        self.assertIsNone(execution_request.input_files)