from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class ItyouqrcodeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ityou.qrcode
        xmlconfig.file(
            'configure.zcml',
            ityou.qrcode,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ityou.qrcode:default')

ITYOU_QRCODE_FIXTURE = ItyouqrcodeLayer()
ITYOU_QRCODE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ITYOU_QRCODE_FIXTURE,),
    name="ItyouqrcodeLayer:Integration"
)
ITYOU_QRCODE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ITYOU_QRCODE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ItyouqrcodeLayer:Functional"
)
