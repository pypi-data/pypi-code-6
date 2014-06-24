# -*- coding: utf-8 -*-
from zope.configuration import xmlconfig
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class RERFixDelete(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import rer.fix13603
        xmlconfig.file('configure.zcml',
                       rer.fix13603,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])

RERFIXDELETE_FIXTURE = RERFixDelete()

RERFIXDELETE_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(RERFIXDELETE_FIXTURE, ),
                       name="RERFixDelete:Functional")
