# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig


class PlonePortletStaticLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import Products.ATContentTypes
        self.loadZCML(package=Products.ATContentTypes)
        z2.installProduct(app, 'Products.Archetypes')
        z2.installProduct(app, 'Products.ATContentTypes')
        z2.installProduct(app, 'plone.portlet.static')
        import plone.portlet.static
        xmlconfig.file(
            'configure.zcml',
            plone.portlet.static,
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.ATContentTypes:default')
        applyProfile(portal, 'plone.portlet.static:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.acl_users.userFolderAddUser(
            'admin',
            'secret',
            ['Manager'],
            []
        )
        portal.invokeFactory(
            "Folder",
            id="test-folder",
            title=u"Test Folder"
        )

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'plone.portlet.static')

PLONEPORTLETSTATIC_FIXTURE = PlonePortletStaticLayer()

PLONEPORTLETSTATIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEPORTLETSTATIC_FIXTURE,),
    name="PloneAppCollectionLayer:Integration"
)
