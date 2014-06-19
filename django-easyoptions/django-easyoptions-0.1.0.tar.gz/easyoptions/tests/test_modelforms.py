from __future__ import absolute_import

from django import forms
from django.db import models
from django.test import TestCase
from django.utils import six

from easyoptions.options import OptionsBase, modelform_options_factory


class TestModel(models.Model):
    field = models.CharField(max_length=20)


class TestOptions(OptionsBase):
    def __init__(self, options):
        self.test_option = options.pop('test_option', None)
        super(TestOptions, self).__init__(options)


class TestForm(six.with_metaclass(
        modelform_options_factory(TestOptions),
        forms.ModelForm)):

    class Meta:
        model = TestModel

    class TestOptions:
        test_option = True


class FormTests(TestCase):

    def test_inheritance(self):
        # Test that the form metaclass was correctly applied
        # The type() of a class is its metaclass, and that metaclass has a
        # __mro__ like all other classes
        self.assertIn(type(forms.ModelForm), type(TestForm).__mro__)

        # Make sure the class heirarchy was not totally destroyed or something
        self.assertTrue(issubclass(TestForm, forms.ModelForm))
        self.assertTrue(issubclass(TestForm, TestForm))

    def test_options(self):
        # Make sure that options are still applied
        self.assertTrue(hasattr(TestForm, '_testoptions'))
        self.assertFalse(hasattr(TestForm, 'TestOptions'))
        self.assertTrue(TestForm._testoptions.test_option)
        self.assertIsInstance(
            TestForm._testoptions,
            TestOptions)

    def test_form(self):
        # Make sure the form still works
        value = 'foo'
        form = TestForm({'field': value})
        self.assertIn('field', form.fields)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertIsInstance(instance, TestModel)
