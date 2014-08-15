from zope.configuration.exceptions import ConfigurationError
from ftw.profilehook.interfaces import IProfileHook
from ftw.profilehook.testing import PROFILEHOOK_INTEGRATION_TESTING
from ftw.profilehook.tests.base import ZCMLIsolationTestCase
from zope.component import getAdapter


def hook(site):
    pass


class TestMetaDirective(ZCMLIsolationTestCase):
    layer = PROFILEHOOK_INTEGRATION_TESTING

    def setUp(self):
        super(TestMetaDirective, self).setUp()
        self.site = self.layer['portal']

    def test_registering_hook_registers_adapter(self):
        self.load_zcml_string(
            '<configure'
            '   xmlns="http://namespaces.zope.org/zope"'
            '   xmlns:five="http://namespaces.zope.org/five"'
            '   xmlns:profilehook="http://namespaces.zope.org/profilehook">'

            ' <include package="ftw.profilehook" />'
            ' <profilehook:hook'
            '     profile="ftw.profilehook.tests:foo"'
            '     handler="{0}.hook"'
            '     />'

            '</configure>'.format(self.__module__))


        self.assertEquals(hook, getAdapter(self.site,
                                           IProfileHook,
                                           name='ftw.profilehook.tests:foo'))
