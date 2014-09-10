from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class PdplonedemograficoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import pd.plonedemografico
        xmlconfig.file(
            'configure.zcml',
            pd.plonedemografico,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pd.plonedemografico:default')

PD_PLONEDEMOGRAFICOFIXTURE = PdplonedemograficoLayer()
PD_PLONEDEMOGRAFICOINTEGRATION_TESTING = IntegrationTesting(
    bases=(PD_PLONEDEMOGRAFICOFIXTURE,),
    name="PdplonedemograficoLayer:Integration"
)
PD_PLONEDEMOGRAFICO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PD_PLONEDEMOGRAFICOFIXTURE, z2.ZSERVER_FIXTURE),
    name="PdplonedemograficoLayer:Functional"
)
