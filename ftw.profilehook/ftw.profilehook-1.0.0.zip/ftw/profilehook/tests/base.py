from plone.testing import zca
from unittest2 import TestCase
from zope.configuration import xmlconfig


class ZCMLIsolationTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(ZCMLIsolationTestCase, self).__init__(*args, **kwargs)
        self._configuration_context = None

    def setUp(self):
        zca.pushGlobalRegistry()

    def tearDown(self):
        zca.popGlobalRegistry()

    def load_zcml_string(self, zcml):
        xmlconfig.string(zcml, context=self._get_configuration_context())

    def _get_configuration_context(self):
        if self._configuration_context is None:
            self._configuration_context = zca.stackConfigurationContext(
                self.layer.get('configurationContext'))
        return self._configuration_context
