from Products.CMFCore.utils import getToolByName
from simplelayout.types.common.testing import INSTALLATION_INTEGRATION_TESTING
from unittest2 import TestCase


class TestInstallation(TestCase):

    layer = INSTALLATION_INTEGRATION_TESTING

    def test_generic_setup_profile_installed(self):
        portal = self.layer['portal']
        portal_setup = getToolByName(portal, 'portal_setup')

        version = portal_setup.getLastVersionForProfile(
            'simplelayout.types.common:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')
