from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import ftw.labels.tests.builders
import logging
import sys


handler = logging.StreamHandler(stream=sys.stderr)
logging.root.addHandler(handler)


class AdaptersZCMLLayer(ComponentRegistryLayer):
    """A layer which only loads the adapters.zcml.
    """

    def setUp(self):
        super(AdaptersZCMLLayer, self).setUp()
        import ftw.labels
        self.load_zcml_file('adapters.zcml', ftw.labels)


ADAPTERS_ZCML_LAYER = AdaptersZCMLLayer()


class LabelsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import ftw.labels
        xmlconfig.file('configure.zcml',
                       ftw.labels,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.labels:default')


LABELS_FIXTURE = LabelsLayer()
LABELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LABELS_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.labels:functional")
