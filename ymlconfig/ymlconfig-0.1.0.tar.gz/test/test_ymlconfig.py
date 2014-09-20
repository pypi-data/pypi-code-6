""" tests for ymlconfig module """
# copyright (c) 2014, Edward F. Wahl.

from bunch import Bunch
import unittest
import ymlconfig

#pylint: disable=R0904,W0212

class TestYmlconfig(unittest.TestCase):
    """
        test ymlconfig
    """

    def setUp(self):
        """ set up tests """
        super().setUp()

    def tearDown(self):
        """ tear down tests """
        super().tearDown()

    def test_bunchify_tree(self):
        """ simple test feature _bunchify_tree """

        data = {'foo':'foo', 'bar': 1}
        data = ymlconfig._bunchify_tree(data)

        self.assertEqual(data.foo, 'foo')
        self.assertEqual(data.bar, 1)
        self.assertIsInstance(data, Bunch)

    def test_bunchify_tree_complex(self):
        """ complex feature _bunchify_tree test """

        data = ['foo',
               {'outer':'val1','inner':
                                {'key1' : 'in1',
                                 'key2' : 'in2'}},
               ['bar', {'listin':'valin'}]]

        data = ymlconfig._bunchify_tree(data)

        self.assertIsInstance(data, list)
        self.assertEqual(data[0], 'foo')
        self.assertIsInstance(data[1], Bunch)
        self.assertIsInstance(data[1].inner, Bunch)
        self.assertEqual(data[1].inner.key1, 'in1')
        self.assertIsInstance(data[2], list)
        self.assertIsInstance(data[2][1], Bunch)
        self.assertEqual(data[2][1].listin, 'valin')

    def test_load(self):
        """ test feature load """

        yamldata = '''
                    key1: 'value1'
                    key2:
                       - 'item1'
                       - 'item2'
                    key3:
                       key31: 'value31'
                       key32: 'value32'
                    '''

        config = ymlconfig.load(yamldata)
        self.assertEqual(config.key1, 'value1')
        self.assertEqual(config.key2[1], 'item2')
        self.assertEqual(config.key3.key31, 'value31')

    def test_format_substitution(self):
        """ test feature test_format with substitution of kwargs"""

        yamldata = '''
                    key1: 'value1'
                    key2:
                        - 'item1'
                        - 'item2'
                    key3: !format
                        format: 'kw1: {kwarg1} kw2: {kwarg2}'
                        kwarg1: 'default1'
                        kwarg2: 'default2'

                    '''

        config = ymlconfig.load(yamldata, kwarg2='fromkw2')
        self.assertEqual(config.key1, 'value1')
        self.assertEqual(config.key3, 'kw1: default1 kw2: fromkw2')

    def test_python_format(self):
        """ test feature test_python_format """

        yamldata = '''
                    key1: &alias1 'value1'
                    key2:
                       - 'item1'
                       - 'item2'
                    key3: !format
                        format: '{arg1} {arg2}'
                        arg1: *alias1
                        arg2: 'arg2'

                    '''

        config = ymlconfig.load(yamldata)
        self.assertEqual(config.key1, 'value1')
        self.assertEqual(config.key3, 'value1 arg2')



