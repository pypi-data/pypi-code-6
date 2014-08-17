import os

from mock import patch

from .base import TestCase

from ..structure import capabilities
from .. import loader


# seperate, blank, replaceable capabilities for each test
@patch.dict(capabilities._internal, clear=True)
class LoaderTestCase(TestCase):

    def test_find_documents(self):
        """ Test that we attempt to load all files in /definitions. """
        # go count the number of files in that directory
        count = 0
        # up two directories (tests, then crowsnest_capabilities)
        for dirpath, child_dirs, filenames in os.walk(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/definitions/'):
            count += len(filenames)

        # make sure this matches the number of documents we find
        documents = loader._find_documents()
        self.assertEqual(count, len(documents))

    def test_combine_documents(self):
        """ Test that we properly detect duplicates and combine the documents. """
        # test that these are combined
        self.assertEqual(loader._combine_documents([
                {'foo': 10},
                {'bar': 20},
                {'baz': 30},
            ]),
            {
                'foo': 10,
                'bar': 20,
                'baz': 30,
            }
        )

        # make sure duplicate keys raise an error
        self.assertRaises(Exception, loader._combine_documents, [
            {'duplicate': 100, 'foo': 10},
            {'duplicate': 200, 'bar': 20},
        ])

    def test_top_level_names(self):
        """ Test that the top level names are valiadated correctly. """

        # missing dot between power and get
        invalid_3 = {
            'action.generic.powerget': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_3)
        self.assertNotIn('action.generic.powerget', capabilities)

        # extra dot
        invalid_5 = {
            'action.generic.power.state.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_5)
        self.assertNotIn('action.generic.power.state.get', capabilities)

        valid = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        # this should go without problem
        loader._build_capabilities(valid)
        self.assertIn('action.generic.power.get', capabilities)

    def test_action_definition(self):
        """ Test that action definitions are validated correclty. """

        invalid_type = {
            'action.generic.power.get': [],
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_type)
        self.assertNotIn('action.gneeric.power.get', capabilities)

        invalid_no_inputs = {
            'action.generic.power.get': {
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_no_inputs)
        self.assertNotIn('action.gneeric.power.get', capabilities)

        invalid_no_outputs = {
            'action.generic.power.get': {
                'inputs': {},
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_no_outputs)
        self.assertNotIn('action.gneeric.power.get', capabilities)

        invalid_no_event = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_no_event)
        self.assertNotIn('action.gneeric.power.get', capabilities)

        invalid_nonexistent_event = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_nonexistent_event)
        self.assertNotIn('action.gneeric.power.get', capabilities)

        valid = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        # this should go without problem
        loader._build_capabilities(valid)
        action = capabilities['action.generic.power.get']
        self.assertListsEquivalent(action.outputs.keys(), ['value'])
        self.assertListsEquivalent(action.inputs.keys(), [])
        self.assertEqual(action.async_generated_event_name, 'event.generic.power.changed')


    def test_event_definition(self):
        """ Test that the event definitions are validated correctly. """

        invalid_type = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': []
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_type)
        self.assertNotIn('action.gneeric.power.event', capabilities)

        invalid_no_outputs = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
            }
        }
        self.assertRaises(AssertionError, loader._build_capabilities, invalid_no_outputs)
        self.assertNotIn('action.gneeric.power.changed', capabilities)

        valid = {
            'action.generic.power.get': {
                'inputs': {},
                'outputs': {
                    'value': [True, False]
                },
                'async_generated_event': 'event.generic.power.changed',
            },
            'event.generic.power.changed': {
                'outputs': {
                    'value': [True, False]
                }
            }
        }
        # this should go without problem
        loader._build_capabilities(valid)
        event = capabilities['event.generic.power.changed']
        self.assertListsEquivalent(event.outputs.keys(), ['value'])


    def test_build_field(self):
        """ Test that fields are validated and built correctly.

        The testing of all the actual permutations is handled in tests/models.py.
        This is just to test the shortcut definitions.
        """

        # ints, floats, booleans, null-values are all disallowed
        invalid_values = [10, 1.1, True, None]
        for invalid_value in invalid_values:
            self.assertRaises(AssertionError, loader._build_field, 'field_name', invalid_value)

        with patch('crowsnest_capabilities.loader.DataField') as MockDataField:
            # ensure strings turn into type args
            loader._build_field('field_name', '//int')
            MockDataField.assert_called_once_with('field_name', type='//int')
            MockDataField.reset_mock()

            # ensure lists turn into valid_values
            loader._build_field('field_name', [0, 1, 2])
            MockDataField.assert_called_once_with('field_name', valid_values=[0, 1, 2])
            MockDataField.reset_mock()

            # ensure default values imply required=False, even when explicitly asked for True
            loader._build_field('field_name', {'default': 33})
            MockDataField.assert_called_once_with('field_name', default=33, required=False)
            MockDataField.reset_mock()

            loader._build_field('field_name', {'default': 33, 'required': True})
            MockDataField.assert_called_once_with('field_name', default=33, required=False)
            MockDataField.reset_mock()
