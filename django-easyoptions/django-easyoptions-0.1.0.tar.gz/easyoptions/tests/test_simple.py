from django.test import TestCase
from django.utils import six
from easyoptions.options import options_factory, OptionsBase


class SimpleOptions(OptionsBase):
    def __init__(self, options):
        self.simple_option = options.pop('simple_option', False)
        super(SimpleOptions, self).__init__(options)



class SimpleBase(six.with_metaclass(options_factory(SimpleOptions), object)):
    pass


class SimpleImplementation(SimpleBase):
    class SimpleOptions:
        simple_option = True

class MissingImplementation(SimpleBase):
    pass


class SimpleChild(SimpleImplementation):
    pass


class GenericTestCase(TestCase):
    def test_simple_class(self):
        self.assertTrue(hasattr(SimpleImplementation, '_simpleoptions'))
        self.assertFalse(hasattr(SimpleImplementation, 'SimpleOptions'))
        self.assertTrue(SimpleImplementation._simpleoptions.simple_option)
        self.assertIsInstance(
            SimpleImplementation._simpleoptions,
            SimpleOptions)

    def test_missing_options(self):
        self.assertFalse(hasattr(MissingImplementation, '_simpleoptions'))
        self.assertFalse(hasattr(MissingImplementation, 'SimpleOptions'))

    def test_inherit_options(self):
        self.assertTrue(hasattr(SimpleChild, '_simpleoptions'))
        self.assertFalse(hasattr(SimpleChild, 'SimpleOptions'))
        self.assertTrue(SimpleChild._simpleoptions.simple_option)
        self.assertIsInstance(
            SimpleImplementation._simpleoptions,
            SimpleOptions)


    def test_incorrect_option(self):
        with self.assertRaises(TypeError):
            class SimpleError(SimpleChild):
                class SimpleOptions:
                    unknown_option = 'booo'
