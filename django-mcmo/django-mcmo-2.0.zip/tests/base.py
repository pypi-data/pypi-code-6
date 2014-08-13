from django.utils import unittest
from django.conf import settings
from django.db.models import loading
from django.utils.datastructures import SortedDict
from django.core import management as management_core
from django.utils import six

from mcmo import management as management_mcmo

# nose should not look for tests in this module
__test__ = False
__unittest = True


NO_SETTING = ('!', None)


class TestSettingsManager(object):
    """
    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Automatically handles resyncing the DB if INSTALLED_APPS is
    modified.
    """

    def __init__(self):
        self._original_settings = {}

    def set(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            self._original_settings.setdefault(k, getattr(settings,
                                                          k, NO_SETTING))
            setattr(settings, k, v)
        if 'INSTALLED_APPS' in kwargs:
            management_mcmo._commands = None
            try:
                # django 1.7 apps registry
                from django.apps.registry import apps
                apps.set_installed_apps(kwargs['INSTALLED_APPS'])
            except ImportError:
                pass
            self.syncdb()

    def syncdb(self):
        loading.cache.loaded = False
        loading.cache.app_store = SortedDict()
        loading.cache.handled = set()
        loading.cache.postponed = []
        loading.cache.nesting_level = 0
        loading.cache._get_models_cache = {}
        loading.cache.available_apps = None

        management_core.call_command('syncdb', verbosity=0)

    def revert(self):
        for k, v in six.iteritems(self._original_settings):
            if v == NO_SETTING:
                delattr(settings, k)
            else:
                setattr(settings, k, v)
        if 'INSTALLED_APPS' in self._original_settings:
            try:
                # django 1.7 apps registry
                from django.apps.registry import apps
                apps.unset_installed_apps()
            except ImportError:
                pass
            self.syncdb()
        self._original_settings = {}


class TestCase(unittest.TestCase):
    """
    A subclass of the Django TestCase with a settings_manager
    attribute which is an instance of TestSettingsManager.

    Comes with a tearDown() method that calls
    self.settings_manager.revert().
    """

    apps = ()

    @classmethod
    def setUpClass(cls):
        cls._apps = ['tests.%s' % a for a in ('app0',) + cls.apps]
        cls.settings_manager = TestSettingsManager()
        cls.settings_manager.set(
            INSTALLED_APPS=settings.INSTALLED_APPS + cls._apps)

    @classmethod
    def tearDownClass(cls):
        cls.settings_manager.revert()

    @classmethod
    def is_in_options(cls, command, option):
        cmd_class = management_core.load_command_class(cls._apps, command)
        return option in [o.get_opt_string() for o in cmd_class.option_list]

    @staticmethod
    def call_command(command, *args, **options):
        management_core.call_command(command, *args, **options)

    def assertInOptions(self, command, option, msg=None):
        if not self.is_in_options(command, option):
            standardMsg = 'Option "%s" does not exist for command %s' \
                          % (option, command)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertNotInOptions(self, command, option, msg=None):
        if self.is_in_options(command, option):
            standardMsg = 'Option "%s" unexpectedly exists for command %s' \
                          % (option, command)
            self.fail(self._formatMessage(msg, standardMsg))
