from unittest import TestCase

from vecnet.simulation import sim_model, Simulation, SimulationGroup


GROUP_DICT = {
    'simulations': [
        {
            'input_files': {
                'foo.txt': 'http://www.example.com/path/to/foo.txt',
                'bar.bin': 'http://file.server.example.com/big/binary/files/bar.bin',
            },
            'cmd_line_args': ['--verbose', '-d', 'path/to/some/folder']
        },
        {
            'input_files': {
                'scenario.xml': 'http://svn.example.com/project/tags/4.3/data/scenario.xml',
            },
            'model': sim_model.OPEN_MALARIA,
            'model_version': 32,
            'cmd_line_args': ['--validate']
        },
        {
            'input_files': {
                'config.json': 'https://www.dropbox.com/s/qmocfrco2t0d28o/config.json?dl=1',
                'campaign.json': 'https://www.dropbox.com/s/qmocfrco2t0d28o/campaign.json?dl=1'
            },
            'model_version': '1.5',
        },
    ],
    'default_model': 'EMOD',
    'default_version': '1.6',
}


class GroupFromDictTests(TestCase):
    """
    Tests of the from_dict class method for SimulationGroup.
    """

    def test_just_required_keys(self):
        """
        Test with just the required keys.
        """
        d = {
            'simulations': None,
        }
        group = SimulationGroup.from_dict(d)
        self.assertEqual(group.simulations, [])
        self.assertIsNone(group.default_model)
        self.assertIsNone(group.default_version)

    def test_all_keys(self):
        """
        Test with all the valid keys.
        """
        d = GROUP_DICT
        group = SimulationGroup.from_dict(d)
        self.assertEqual(len(group.simulations), len(d['simulations']))
        for simulation, src_dict in zip(group.simulations, d['simulations']):
            self.assertDictContainsSubset(src_dict, simulation.to_dict())
        self.assertEqual(group.default_model, d['default_model'])
        self.assertEqual(group.default_version, d['default_version'])


class GroupToDictTests(TestCase):
    """
    Tests of the to_dict method for SimulationGroup.
    """

    def test_empty_group(self):
        """
        Test with a simulation group with empty attributes.
        """
        group = SimulationGroup()
        expected_dict = {
            'simulations': [],
            'default_model': None,
            'default_version': None,
        }
        self.assertEqual(group.to_dict(), expected_dict)

    def test_group_with_data(self):
        """
        Test with a simulation group whose attributes aren't empty.
        """
        simulations = [Simulation.from_dict(d) for d in GROUP_DICT['simulations']]
        group = SimulationGroup(simulations=simulations,
                                default_model=GROUP_DICT['default_model'],
                                default_version=GROUP_DICT['default_version'])
        d = group.to_dict()
        for key in ('default_model', 'default_version'):
            self.assertEqual(d[key], GROUP_DICT[key])
        self.assertEqual(len(d['simulations']), len(GROUP_DICT['simulations']))
        for actual_dict, expected_dict in zip(d['simulations'], GROUP_DICT['simulations']):
            self.assertDictContainsSubset(expected_dict, actual_dict)
