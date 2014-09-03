from mock import patch

from .base import TestCase

from ..structure import capabilities, _Capabilities, _flatten
from ..models import Action, Event, DataField


# some test models
test_power_get = Action('action.generic.power.get', inputs={}, outputs={'value': DataField('value', valid_values=[True, False])}, async_generated_event_name='event.generic.power.changed')
test_power_set = Action('action.generic.power.set', inputs={'value': DataField('value', valid_values=[True, False])}, outputs={}, async_generated_event_name='event.generic.power.changed')
test_power_changed = Event('event.generic.power.changed', outputs={'value': DataField('value', valid_values=[True, False])})

test_internal = {
    'action': {
        'generic': {
            'power': {
                'get': test_power_get,
                'set': test_power_set,
            }
        }
    },
    'event': {
        'generic': {
            'power': {
                'changed': test_power_changed
            }
        }
    }
}


class CapabilitiesTestCase(TestCase):

    def test_flatten(self):
        """ Test that the _flatten() helper works. """
        self.assertListsEquivalent(_flatten({}), [])
        self.assertListsEquivalent(_flatten({'a': 1, 's': 2, 'd': 3}), [1, 2, 3])
        self.assertListsEquivalent(_flatten({
            'a': 1,
            's': {
                'd': 2
            },
            'f': {
                'j': {
                    'k': 3
                }
            }
        }), [1, 2, 3])

    @patch.object(_Capabilities, '_already_loaded', False)
    @patch('crowsnest_capabilities.structure.loader')
    def test_ensure_loaded(self, mock_loader):
        capabilities.ensure_loaded()

        # make sure we called load()
        mock_loader.load.assert_called_once_with()

        # make sure _already_loaded is now true
        self.assertTrue(capabilities._already_loaded)

        # make sure another attempt at ensure_loaded() does not re-run load()
        capabilities.ensure_loaded()
        mock_loader.load.assert_called_once()

    @patch.object(capabilities, '_internal', test_internal)
    @patch.object(_Capabilities, '_already_loaded', True)
    def test_traverse(self):
        steps = ['action', 'generic', 'power', 'get']
        power_get = capabilities._traverse(steps)
        self.assertIs(power_get, capabilities._internal['action']['generic']['power']['get'])

    @patch.object(capabilities, '_internal', test_internal)
    @patch.object(_Capabilities, '_already_loaded', True)
    def test_get_item(self):
        """ Test magic lookups with __getitem__ """
        power_get = capabilities['action.generic.power.get']
        self.assertIs(power_get, capabilities._internal['action']['generic']['power']['get'])

    @patch.object(capabilities, '_internal', test_internal)
    @patch.object(_Capabilities, '_already_loaded', True)
    def test_set_item(self):
        """ Test magic setting with __setitem__ """
        fake = Action('action.generic.power.fake', {}, {}, '')
        try:
            capabilities[fake.name] = fake
            self.assertIs(fake, capabilities._internal['action']['generic']['power']['fake'])
        finally:
            # clean this up
            del capabilities._internal['action']['generic']['power']['fake']

    @patch.object(capabilities, '_internal', test_internal)
    @patch.object(_Capabilities, '_already_loaded', True)
    def test_contains(self):
        """ Test magic 'in' testing with __contains__ """
        # set up our assumptions
        capabilities.ensure_loaded()

        self.assertIn('action', capabilities._internal)
        self.assertIn('generic', capabilities._internal['action'])
        self.assertIn('power', capabilities._internal['action']['generic'])
        self.assertIn('get', capabilities._internal['action']['generic']['power'])

        # actual test
        self.assertIn('action.generic.power.get', capabilities)

    @patch.object(capabilities, '_internal', test_internal)
    @patch.object(_Capabilities, '_already_loaded', True)
    def test_group(self):
        """ Test group() lookup """
        self.assertListsEquivalent(
            capabilities.group(),
            [test_power_get, test_power_set, test_power_changed]
        )
        self.assertListsEquivalent(
            capabilities.group('action'),
            [test_power_get, test_power_set]
        )
        self.assertListsEquivalent(
            capabilities.group('event'),
            [test_power_changed]
        )
        self.assertListsEquivalent(
            capabilities.group('action.generic'),
            [test_power_get, test_power_set]
        )
        self.assertListsEquivalent(
            capabilities.group('event.generic'),
            [test_power_changed]
        )
        self.assertListsEquivalent(
            capabilities.group('action.generic.power'),
            [test_power_get, test_power_set]
        )
        self.assertListsEquivalent(
            capabilities.group('event.generic.power'),
            [test_power_changed]
        )
        self.assertListsEquivalent(
            capabilities.group('action.generic.power.get'),
            [test_power_get]
        )
        self.assertListsEquivalent(
            capabilities.group('action.generic.power.set'),
            [test_power_set]
        )
        self.assertListsEquivalent(
            capabilities.group('event.generic.power.changed'),
            [test_power_changed]
        )

    def test_class_sharing(self):
        """ Make sure that _internal is shared across instances of _Capabilities """
        # _internal is an object, so identity is testable with "is"
        # instance to class
        self.assertIs(capabilities._internal, _Capabilities._internal)
        # instance to new instance
        self.assertIs(capabilities._internal, _Capabilities()._internal)
