from ftw.profilehook.testing import PROFILEHOOK_INTEGRATION_TESTING
from ftw.profilehook.tests.base import ZCMLIsolationTestCase
from plone.app.testing import applyProfile
from Products.CMFCore.utils import getToolByName


class CallCounter(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.calls = 0

    def __call__(self, site):
        self.calls += 1


call_counter = CallCounter()


class TestIntegration(ZCMLIsolationTestCase):
    layer = PROFILEHOOK_INTEGRATION_TESTING

    def tearDown(self):
        super(TestIntegration, self).tearDown()
        call_counter.reset()

    def test_hook_is_called_when_profile_is_imported(self):
        self.load_zcml_string(
            '<configure'
            '    package="ftw.profilehook.tests"'
            '    xmlns="http://namespaces.zope.org/zope"'
            '    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"'
            '    xmlns:i18n="http://namespaces.zope.org/i18n"'
            '    xmlns:profilehook="http://namespaces.zope.org/profilehook"'
            '    i18n_domain="ftw.profilehook">'

            '  <genericsetup:registerProfile'
            '      name="foo"'
            '      title="ftw.profilehook.tests"'
            '      directory="profiles/foo"'
            '      provides="Products.GenericSetup.interfaces.EXTENSION"'
            '      />'

            '  <include package="ftw.profilehook" />'
            '  <profilehook:hook'
            '      profile="ftw.profilehook.tests:foo"'
            '      handler="{0}.call_counter"'
            '      />'
            '</configure>'.format(self.__module__))

        applyProfile(
            self.layer['portal'], 'ftw.profilehook.tests:foo')

        self.assertEquals(1, call_counter.calls)

    def test_hook_is_not_called_when_other_objects_are_imported(self):
        self.load_zcml_string(
            '<configure'
            '    package="ftw.profilehook.tests"'
            '    xmlns="http://namespaces.zope.org/zope"'
            '    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"'
            '    xmlns:i18n="http://namespaces.zope.org/i18n"'
            '    xmlns:profilehook="http://namespaces.zope.org/profilehook"'
            '    i18n_domain="ftw.profilehook">'

            '  <genericsetup:registerProfile'
            '      name="foo"'
            '      title="ftw.profilehook.tests"'
            '      directory="profiles/foo"'
            '      provides="Products.GenericSetup.interfaces.EXTENSION"'
            '      />'

            '  <include package="ftw.profilehook" />'
            '  <profilehook:hook'
            '      profile="ftw.profilehook.tests:bar"'
            '      handler="{0}.call_counter"'
            '      />'
            '</configure>'.format(self.__module__))

        applyProfile(
            self.layer['portal'], 'ftw.profilehook.tests:foo')

        self.assertEquals(0, call_counter.calls)

    def test_hook_is_not_called_when_not_all_import_steps_are_executed(self):
        self.load_zcml_string(
            '<configure'
            '    package="ftw.profilehook.tests"'
            '    xmlns="http://namespaces.zope.org/zope"'
            '    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"'
            '    xmlns:i18n="http://namespaces.zope.org/i18n"'
            '    xmlns:profilehook="http://namespaces.zope.org/profilehook"'
            '    i18n_domain="ftw.profilehook">'

            '  <genericsetup:registerProfile'
            '      name="foo"'
            '      title="ftw.profilehook.tests"'
            '      directory="profiles/foo"'
            '      provides="Products.GenericSetup.interfaces.EXTENSION"'
            '      />'

            '  <include package="ftw.profilehook" />'
            '  <profilehook:hook'
            '      profile="ftw.profilehook.tests:foo"'
            '      handler="{0}.call_counter"'
            '      />'
            '</configure>'.format(self.__module__))

        profile_id = 'profile-ftw.profilehook.tests:foo'
        setup_tool = getToolByName(self.layer['portal'], 'portal_setup')

        setup_tool.runImportStepFromProfile(profile_id, 'actions')
        self.assertEquals(0, call_counter.calls)

        setup_tool.runAllImportStepsFromProfile(profile_id)
        self.assertEquals(1, call_counter.calls)
