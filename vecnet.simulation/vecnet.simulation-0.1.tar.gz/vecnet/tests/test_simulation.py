from unittest import TestCase

from vecnet.simulation import sim_model, Simulation


class SimulationFromDictTests(TestCase):
    """
    Tests of the from_dict class method for Simulation.
    """

    def test_just_required_keys(self):
        """
        Test with just the required keys.
        """
        d = {
            'input_files': None,
        }
        simulation = Simulation.from_dict(d)
        self.assertEqual(simulation.input_files, {})
        self.assertIsNone(simulation.model)
        self.assertIsNone(simulation.model_version)
        self.assertEqual(simulation.cmd_line_args, [])
        self.assertEqual(simulation.id_on_client, '')

    def test_all_keys(self):
        """
        Test with all the valid keys.
        """
        d = {
            'input_files': {
                'foo.txt': 'http://www.example.com/path/to/foo.txt',
                'bar.bin': 'http://file.server.example.com/big/binary/files/bar.bin',
            },
            'model': sim_model.OPEN_MALARIA,
            'model_version': 32,
            'cmd_line_args': ['--verbose', '-d', 'path/to/some/folder'],
            'id_on_client': '7890',
        }
        simulation = Simulation.from_dict(d)
        self.assertEqual(simulation.input_files, d['input_files'])
        self.assertIsNot(simulation.input_files, d['input_files'])  # Confirm they are copies, not the same object
        self.assertEqual(simulation.model, d['model'])
        self.assertEqual(simulation.model_version, d['model_version'])
        self.assertEqual(simulation.cmd_line_args, d['cmd_line_args'])
        self.assertIsNot(simulation.cmd_line_args, d['cmd_line_args'])  # Confirm they are copies, not the same object
        self.assertEqual(simulation.id_on_client, d['id_on_client'])

    def test_some_keys(self):
        """
        Test with some optional keys, but not all of them.
        """
        d = {
            'input_files': {
                'foo.txt': 'http://www.example.com/path/to/foo.txt',
                'bar.bin': 'http://file.server.example.com/big/binary/files/bar.bin',
            },
            'model': sim_model.OPEN_MALARIA,
        }
        simulation = Simulation.from_dict(d)
        self.assertEqual(simulation.input_files, d['input_files'])
        self.assertIsNot(simulation.input_files, d['input_files'])  # Confirm they are copies, not the same object
        self.assertEqual(simulation.model, d['model'])
        self.assertIsNone(simulation.model_version)
        self.assertIsNot(simulation.cmd_line_args, [])
        self.assertEqual(simulation.id_on_client, '')


class SimulationToDictTests(TestCase):
    """
    Tests of the to_dict method for Simulation.
    """

    def test_empty_simulation(self):
        """
        Test with a simulation with empty attributes.
        """
        simulation = Simulation()
        expected_dict = {
            'input_files': {},
            'model': None,
            'model_version': None,
            'cmd_line_args': [],
            'id_on_client': '',
            'output_url': None,
        }
        self.assertEqual(simulation.to_dict(), expected_dict)

    def test_full_simulation(self):
        """
        Test with a full (typical) simulation.
        """
        expected_dict = {
            'input_files': {
                'foo.txt': 'http://www.example.com/path/to/foo-v1.2.txt',
                'bar.bin': 'http://file.server.example.com/big/binary/files/bar.bin',
            },
            'model': sim_model.OPEN_MALARIA,
            'model_version': 32,
            'cmd_line_args': ['--verbose', '-d', 'path/to/some/folder'],
            'id_on_client': 'whatever',
            'output_url': 'http://ingester.example.com/simulation-output/',
        }
        simulation = Simulation(**expected_dict)
        d = simulation.to_dict()
        self.assertEqual(d, expected_dict)
        for key in ('input_files', 'cmd_line_args'):
            self.assertIsNot(d[key], expected_dict[key])  # Confirm they are copies, not the same object
