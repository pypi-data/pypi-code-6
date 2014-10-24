# -*- coding: utf-8 -*-

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import interlegis.intranetmodelo.departments
        self.loadZCML(package=interlegis.intranetmodelo.departments)

    def setUpPloneSite(self, portal):
        self.applyProfile(
            portal, 'interlegis.intranetmodelo.departments:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='interlegis.intranetmodelo.departments:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='interlegis.intranetmodelo.departments:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='interlegis.intranetmodelo.departments:Robot',
)
