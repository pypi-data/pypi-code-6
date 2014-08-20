# -*- coding:utf-8 -*-
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
)
from plone.testing import z2
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE


class JazzportTests(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.jazzport
        self.loadZCML(package=collective.jazzport)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        self.applyProfile(
            portal, 'collective.jazzport:default')


JAZZPORT_FIXTURE = JazzportTests()

JAZZPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JAZZPORT_FIXTURE,),
    name='JazzportTests:Integration')

JAZZPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JAZZPORT_FIXTURE,),
    name='JazzportTests:Functional')

JAZZPORT_ROBOT_TESTING = FunctionalTesting(
    bases=(JAZZPORT_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER),
    name='JazzportTests:Robot')
