import unittest
from nose.tools import *
from mako.template import Template
from mako_sugar import convert_calls, convert_defs, convert_imports
from test.util import result_lines

class NamespaceTest(unittest.TestCase):
    
    inputs = """
        % import /components.html as comp
        % from /components.mako import link_to_modal
        % from /components.html import comp1, comp2
        % import customer.lib.presenters as p
        % import ${context['namespace_name']} as dyn
    """.split('\n')
    
    outputs = """
        <%namespace name="comp" file="/components.html" />
        <%namespace file="/components.mako" import="link_to_modal" />
        <%namespace file="/components.html" import="comp1, comp2" />
        <%namespace name="p" module="customer.lib.presenters" />
        <%namespace name="dyn" file="${context['namespace_name']}" />
    """.split('\n')
    
    def test_preprocess(self):
        for inp, out in zip(self.inputs, self.outputs):
            a = result_lines(convert_imports(inp))
            b = result_lines(out)
            assert_equals(a, b)
    
class DefTest(unittest.TestCase):
    def test_preprocess(self):
        t = """
        % def foo():
            hi
        % enddef
        """
        s = """
        <%def name="foo()">
            hi
        </%def>
        """
        t = convert_defs(t)
        assert_equals(result_lines(t), result_lines(s))

class Calltest(unittest.TestCase):    
    def test_preprocess(self):
        t = """
        % call foo():
            hi
        % endcall
        """
        s = """
        <%call expr="foo()">
            hi
        </%call>
        """
        t = convert_calls(t)
        assert_equals(result_lines(t), result_lines(s))
        
    def test_preprocess2(self):
        t = """
        %call foo():
            hi
        %endcall
        """
        s = """
        <%call expr="foo()">
            hi
        </%call>
        """
        t = convert_calls(t)
        assert_equals(result_lines(t), result_lines(s))
        
    def test_call(self):
        t = Template("""
        <%def name="foo()">
            foo
            ${caller.body()}
            foo
        </%def>

        % call foo():
            bar
        % endcall
        """, preprocessor=convert_calls)

        assert_equals(result_lines(t.render()), ['foo', 'bar', 'foo'])