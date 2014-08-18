import sys

from django.conf import settings
from setmagic.backend import SettingsBackend


try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


class SettingsWrapper(object):

    '''
    A magic wrapper for all registered settings
    '''

    def __init__(self):
        super(SettingsWrapper, self).__setattr__('_backend', None)

    def _sync(self):
        '''
        Lazily load the backend
        '''
        if self._backend and 'test' not in sys.argv:
            return

        # Cache all setting defs into a single dict
        super(SettingsWrapper, self).__setattr__('defs', OrderedDict())
        for group_label, setting_defs in settings.SETMAGIC_SCHEMA:
            for setting_def in setting_defs:
                setting_def['group_label'] = group_label
                self.defs[setting_def['name']] = setting_def

        super(SettingsWrapper, self).__setattr__(
            '_backend', SettingsBackend(self.defs))

    def __getattr__(self, name):
        self._sync()
        return self._backend.get(name)

    def __setattr__(self, name, value):
        self._sync()
        self._backend.set(name, value)
