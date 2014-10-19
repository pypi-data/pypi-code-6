# Copyright (c) 2014 Susam Pal
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Tests for don module."""


import unittest
import don


class DONTest(unittest.TestCase):

    def test_parse(self):
        o = don.parse('a: foo\nb: bar')
        self.assertEqual(o, {'a': 'foo', 'b': 'bar'})
        self.assertEqual(o.a, 'foo')
        self.assertEqual(o.b, 'bar')

    def test_parse_file(self):
        o = don.parse_file('test/data/don.cfg')
        self.assertEqual(o, {'a': 'foo', 'b': 'bar'})
        self.assertEqual(o.a, 'foo')
        self.assertEqual(o.b, 'bar')


class ParserTest(unittest.TestCase):
    
    def test_parse(self):
        parser = don.Parser()
        parser.parse('a: foo\nb: bar')
        self.assertEqual(parser.root, {'a': 'foo', 'b': 'bar'})
        self.assertEqual(parser.root.a, 'foo')
        self.assertEqual(parser.root.b, 'bar')

    def test_parse_file(self):
        parser = don.Parser()
        parser.parse_file('test/data/don.cfg')
        self.assertEqual(parser.root, {'a': 'foo', 'b': 'bar'})
        self.assertEqual(parser.root.a, 'foo')
        self.assertEqual(parser.root.b, 'bar')

    def test_simple_don(self):
        parser = don.Parser()
        parser.parse('a: foo')
        self.assertEqual(parser.root, {'a': 'foo'})
        self.assertEqual(parser.root.a, 'foo')

    def test_blank_lines(self):
        parser = don.Parser()
        parser.parse('\na: foo\n')
        self.assertEqual(parser.root, {'a': 'foo'})
        self.assertEqual(parser.root.a, 'foo')
        parser = don.Parser()
        parser.parse('  \na: foo\n  ')
        self.assertEqual(parser.root, {'a': 'foo'})
        self.assertEqual(parser.root.a, 'foo')

    def test_comments(self):
        parser = don.Parser()
        parser.parse('# comment\na: foo\n')
        self.assertEqual(parser.root, {'a': 'foo'})
        self.assertEqual(parser.root.a, 'foo')
        parser = don.Parser()
        parser.parse('  # comment\na: foo\n')
        self.assertEqual(parser.root, {'a': 'foo'})
        self.assertEqual(parser.root.a, 'foo')

    def test_key_declaration(self):
        parser = don.Parser()
        parser.parse('a:\n')
        self.assertEqual(parser.root, {})

    def test_token_validation(self):
        don.Parser().parse('a:')
        don.Parser().parse('_a:')
        don.Parser().parse('_a1:')

        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('1a:')
        self.assertEqual(str(cm.exception),
                         "<str>:1: Invalid token '1a' in key '1a'")

        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a$:')
        self.assertEqual(str(cm.exception),
                         "<str>:1: Invalid token 'a$' in key 'a$'")

        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('foo.bar.1a:')
        self.assertEqual(str(cm.exception),
                         "<str>:1: Invalid token '1a' in key 'foo.bar.1a'")

    def test_nested_don(self):
        parser = don.Parser()
        parser.parse("""a.b.c: foo
                        a.b.d: bar""") 
        self.assertEqual(parser.root,
                         {'a': {'b': {'c': 'foo',
                                      'd': 'bar'}}})
        self.assertEqual(parser.root.a, {'b': {'c': 'foo',
                                               'd': 'bar'}})
        self.assertEqual(parser.root.a.b, {'c': 'foo', 'd': 'bar'})
        self.assertEqual(parser.root.a.b.c, 'foo')
        self.assertEqual(parser.root.a.b.d, 'bar')

    def test_empty_tokens(self):
        parser = don.Parser()
        parser.parse("""a:
                        .b: foo""")
        self.assertEqual(parser.root, {'a': {'b': 'foo'}})
        self.assertEqual(parser.root.a, {'b': 'foo'})
        self.assertEqual(parser.root.a.b, 'foo')

    def test_empty_token_after_nonempty_token(self):
        with self.assertRaises(don.Error) as cm:
            parser = don.Parser()
            parser.parse("""a.b.c: foo
                            .b.: foo""")
        self.assertEqual(str(cm.exception),
                         "<str>:2: Invalid token '' in key '.b.'")

    def test_too_many_empty_tokens(self):
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse("""a: foo
                                  ..b: bar""")
        self.assertEqual(str(cm.exception),
                         "<str>:2: Number of empty tokens in key '..b' "
                         "exceeds number of tokens in the previous key 'a'")

    def test_error_location(self):
        # When DON string is parsed
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a: foo\nb: bar\nc\nd: baz')
        self.assertEqual(str(cm.exception),
                         "<str>:3: Cannot split 'c' into key and value")
        # When DON file is parsed
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse_file('test/data/err.cfg')
        self.assertEqual(str(cm.exception),
                         "test/data/err.cfg:3: "
                         "Cannot split 'c' into key and value")

    def test_no_key_value(self):
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a')
        self.assertEqual(str(cm.exception),
                         "<str>:1: Cannot split 'a' into key and value")

    def test_redefinition_error(self):
        # Simple redefinition
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a: foo\na: foo')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot redefine key 'a' "
                         "with value 'foo' to value 'foo'")

        # Redefinition with some empty tokens
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.a: foo\n.a: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot redefine key 'a.a' "
                         "with value 'foo' to value 'bar'")

        # Redefinition with all empty tokens
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.a: foo\n.: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot redefine key 'a.a' "
                         "with value 'foo' to value 'bar'")

        # Redefinition of a partial key
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.b.c: foo\na.b: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot redefine key 'a.b' "
                         "with value {'c': 'foo'} to value 'bar'")

        # Redefinition of a string value to an object
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.b: foo\na.b.c: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot define 'a.b.c' "
                         "with value 'bar' because 'a.b' is "
                         "already defined with value 'foo'")

        # Redefinition of a string value to a nested object
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.b: foo\na.b.c.d: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot define 'a.b.c.d' "
                         "with value 'bar' because 'a.b' is "
                         "already defined with value 'foo'")

        # Redefinition of a string value to an object with empty tokens
        with self.assertRaises(don.Error) as cm:
            don.Parser().parse('a.b: foo\n..c: bar')
        self.assertEqual(str(cm.exception),
                         "<str>:2: Cannot define 'a.b.c' "
                         "with value 'bar' because 'a.b' is "
                         "already defined with value 'foo'")

    def test_definition_after_declaration(self):
        parser = don.Parser()
        parser.parse('a:\na: foo')
        self.assertEqual(parser.root, {'a': 'foo'})
