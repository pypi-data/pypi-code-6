from OFS.interfaces import IApplication
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.jar import LabelJar
from ftw.labels.testing import ADAPTERS_ZCML_LAYER
from ftw.testing import MockTestCase


class TestJarDiscovery(MockTestCase):
    layer = ADAPTERS_ZCML_LAYER

    def test_adapting_root_returns_jar(self):
        root = self.providing_stub(ILabelRoot)
        self.replay()
        jar = ILabelJar(root)
        self.assertIsInstance(jar, LabelJar)

    def test_walks_up_the_acquisition_for_finding_jar(self):
        root = self.providing_stub(ILabelRoot)
        folder = self.set_parent(self.stub(), root)
        document =  self.set_parent(self.stub(), folder)
        self.replay()

        jar = ILabelJar(document)
        self.assertIsInstance(jar, LabelJar)
        self.assertEquals(root, jar.context)

    def test_raise_when_app_is_reached(self):
        app = self.providing_stub(IApplication)
        document = self.set_parent(self.stub(), app)
        self.replay()

        with self.assertRaises(LookupError) as cm:
            ILabelJar(document)

        self.assertEquals(
            'Could not find ILabelJar on any parents.'
            ' No parent seems to provide ILabelRoot.',
            str(cm.exception))
