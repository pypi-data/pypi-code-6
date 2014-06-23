from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.jar import LabelJar
from ftw.labels.testing import ADAPTERS_ZCML_LAYER
from zope.annotation import IAttributeAnnotatable
from zope.component import queryAdapter
from plone.mocktestcase.dummy import Dummy
from zope.interface.verify import verifyClass
from unittest2 import TestCase
from zope.interface import alsoProvides


class TestLabelJar(TestCase):
    layer = ADAPTERS_ZCML_LAYER

    def setUp(self):
        self.root = Dummy()
        alsoProvides(self.root, ILabelRoot, IAttributeAnnotatable)

    def test_label_jar_implements_interface(self):
        self.assertTrue(ILabelJar.implementedBy(LabelJar),
                        'LabelJar should implement ILabelJar')
        verifyClass(ILabelJar, LabelJar)

    def test_adapter_is_registered_for_label_root(self):
        self.assertTrue(
            queryAdapter(self.root, ILabelJar),
            'The LabelJar adapter is not registered for ILabelRoot')

    def test_adding_new_label(self):
        jar = LabelJar(self.root)
        label_id = jar.add('Question', '#FF0000')

        self.assertDictEqual({'label_id': label_id,
                              'title': 'Question',
                              'color': '#FF0000'},
                             jar.get(label_id))

    def test_label_ids_are_unique(self):
        jar = LabelJar(self.root)

        first_label_id = jar.add('Question', '#FF0000')
        second_label_id = jar.add('Question', '#FF0000')

        self.assertNotEquals(second_label_id, first_label_id,
                             'Labels ID should be unique.')

    def test_listing_labels(self):
        jar = LabelJar(self.root)

        first_label_id = jar.add('First', '#FF0000')
        second_label_id = jar.add('Second', '#0000FF')

        self.assertItemsEqual(
            [{'label_id': first_label_id,
              'title': 'First',
              'color': '#FF0000'},
             {'label_id': second_label_id,
              'title': 'Second',
              'color': '#0000FF'}],
            jar.list())

    def test_listing_labels_is_sorted(self):
        jar = LabelJar(self.root)

        jar.add('Zeta-0', '')
        jar.add('zeta-1', '')
        jar.add('alpha-0', '')
        jar.add('\xc3\x84lpha-1', '')
        jar.add('Alpha-2', '')

        self.assertEqual(
            ['alpha-0', '\xc3\x84lpha-1', 'Alpha-2', 'Zeta-0', 'zeta-1'],
            [label.get('title') for label in jar.list()])

    def test_updating_labels(self):
        jar = LabelJar(self.root)

        label_id = jar.add('Question', '#FF0000')
        self.assertDictEqual({'label_id': label_id,
                              'title': 'Question',
                              'color': '#FF0000'},
                             jar.get(label_id))

        jar.update(label_id, 'New Question', '#0000FF')
        self.assertDictEqual({'label_id': label_id,
                              'title': 'New Question',
                              'color': '#0000FF'},
                             jar.get(label_id))

    def test_remove_labels(self):
        jar = LabelJar(self.root)

        label_id = jar.add('Question', '#FF0000')
        self.assertEqual(
            [{'label_id': label_id,
              'title': 'Question',
              'color': '#FF0000'}],
            jar.list())

        jar.remove(label_id)
        self.assertEqual([], jar.list())

    def test_label_dict_mutations_are_not_stored(self):
        jar = LabelJar(self.root)
        label_id = jar.add('Question', '#FF0000')

        label = jar.get(label_id)
        label['title'] = 'HACK THE TITLE'

        self.assertDictEqual({'label_id': label_id,
                              'title': 'Question',
                              'color': '#FF0000'},
                             jar.get(label_id))

    def test_list_mutations_are_not_stored(self):
        jar = LabelJar(self.root)
        label_id = jar.add('Question', '#FF0000')

        labels = jar.list()
        self.assertEqual(
            [{'label_id': label_id,
              'title': 'Question',
              'color': '#FF0000'}],
            labels)

        del labels[0]
        self.assertEqual(
            [{'label_id': label_id,
              'title': 'Question',
              'color': '#FF0000'}],
            jar.list())

    def test_data_is_stored_persistently(self):
        jar = LabelJar(self.root)

        label_id = jar.add('Question', '#FF0000')
        self.assertEqual(
            [{'label_id': label_id,
              'title': 'Question',
              'color': '#FF0000'}],
            jar.list())

        jar = LabelJar(self.root)
        self.assertEqual(
            [{'label_id': label_id,
              'title': 'Question',
              'color': '#FF0000'}],
            jar.list())
