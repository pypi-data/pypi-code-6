# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, PLONE_FIXTURE, IntegrationTesting, FunctionalTesting
from plone.testing import z2
from plone.app.testing import quickInstallProduct

class EKEReview(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import eke.review
        self.loadZCML(package=eke.review)
        z2.installProduct(app, 'eke.review')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'eke.review:default')
        quickInstallProduct(portal, 'Products.PloneFormGen')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'eke.review')


EKE_REVIEW_FIXTURE = EKEReview()
EKE_REVIEW_INTEGRATION_TESTING = IntegrationTesting(bases=(EKE_REVIEW_FIXTURE,), name='EKEReview:Integration')
EKE_REVIEW_FUNCTIONAL_TESTING = FunctionalTesting(bases=(EKE_REVIEW_FIXTURE,), name='EKEReview:Functional')
