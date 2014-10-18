import unittest
from nose.tools import *
from mako.template import Template
from mako_sugar import sugar
from test.util import result_lines

class SugarTest(unittest.TestCase):
    def test_sugar(self):
        in_call = """
        %call foo():
            hi
        %endcall
        """
        in_def = """
        %def foo():
            hi
        %enddef
        """
        in_import = """
        %import /foo as foo
        """
        
        sugar_all = sugar()
        assert_not_equal(sugar_all(in_call), in_call)
        assert_not_equal(sugar_all(in_def), in_def)
        assert_not_equal(sugar_all(in_import), in_import)
        
        sugar_no_call = sugar(exclude=['call'])
        assert_equal(sugar_no_call(in_call), in_call)
        assert_not_equal(sugar_no_call(in_def), in_def)
        assert_not_equal(sugar_no_call(in_import), in_import)
        
        sugar_no_def = sugar(exclude=['def'])
        assert_not_equal(sugar_no_def(in_call), in_call)
        assert_equal(sugar_no_def(in_def), in_def)
        assert_not_equal(sugar_no_def(in_import), in_import)