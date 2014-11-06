from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class PdprenotazioniLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import pd.prenotazioni
        xmlconfig.file(
            'configure.zcml',
            pd.prenotazioni,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pd.prenotazioni:default')

PD_PRENOTAZIONI_FIXTURE = PdprenotazioniLayer()
PD_PRENOTAZIONI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PD_PRENOTAZIONI_FIXTURE,),
    name="PdprenotazioniLayer:Integration"
)
PD_PRENOTAZIONI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PD_PRENOTAZIONI_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PdprenotazioniLayer:Functional"
)
