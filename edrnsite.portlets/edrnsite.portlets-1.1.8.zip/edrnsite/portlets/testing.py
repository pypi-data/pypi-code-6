# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, PLONE_FIXTURE, IntegrationTesting, FunctionalTesting
from plone.testing import z2
from plone.app.testing import setRoles, login, TEST_USER_ID, TEST_USER_NAME

class EDRNSitePortlets(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import edrnsite.portlets
        self.loadZCML(package=edrnsite.portlets)
        z2.installProduct(app, 'edrnsite.portlets')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'edrnsite.portlets:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder', title=u'Test Folder')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'edrnsite.portlets')


EDRNSITE_PORTLETS_FIXTURE = EDRNSitePortlets()
EDRNSITE_PORTLETS_INTEGRATION_TESTING = IntegrationTesting(bases=(EDRNSITE_PORTLETS_FIXTURE,), name='EDRNSitePortlets:Integration')
EDRNSITE_PORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(bases=(EDRNSITE_PORTLETS_FIXTURE,), name='EDRNSitePortlets:Functional')
