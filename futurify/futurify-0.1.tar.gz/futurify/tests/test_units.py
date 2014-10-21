from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path

from unittest import TestCase

from .. import find_future_imports, make_new_import_statement

__here__ = os.path.dirname(__file__)
examples = os.path.join(__here__, 'examples')


class TestFindFutureImports(TestCase):

    def test_simple(self):
        fn = os.path.join(examples, 'simple.py')
        with open(fn) as f:
            found = list(find_future_imports(f))
        self.assertEqual(len(found), 1)
        start, end, imports = found[0]
        self.assertEqual(start, 1)
        self.assertEqual(end, 1)
        self.assertEqual(['print_function', 'absolute_import'], imports)

    def test_multiline(self):
        fn = os.path.join(examples, 'multiline.py')
        with open(fn) as f:
            found = list(find_future_imports(f))
        self.assertEqual(len(found), 2)

        start, end, imports = found[0]
        self.assertEqual(start, 2)
        self.assertEqual(end, 3)
        self.assertEqual(['print_function', 'division'], imports)

        start, end, imports = found[1]
        self.assertEqual(start, 6)
        self.assertEqual(end, 6)
        self.assertEqual(['absolute_import'], imports)

    def test_complex(self):
        fn = os.path.join(examples, 'complex.py')
        with open(fn) as f:
            found = list(find_future_imports(f))
        self.assertEqual(len(found), 1)

        start, end, imports = found[0]
        self.assertEqual(start, 13)
        self.assertEqual(end, 17)
        self.assertEqual(['with_statement', 'print_function',
                          'absolute_import'], imports)

    def test_no_imports(self):
        fn = os.path.join(examples, 'no_imports.py')
        with open(fn) as f:
            found = list(find_future_imports(f))
        self.assertEqual(found, [])


class TestMakeNewImportStatement(TestCase):

    def test_simple(self):
        s = make_new_import_statement(['print_function'])
        self.assertEqual(s, 'from __future__ import print_function')

    def test_multiple(self):
        s = make_new_import_statement(['print_function', 'division'])
        self.assertEqual(s, 'from __future__ import division, print_function')

    def test_multiline(self):
        s = make_new_import_statement(['print_function', 'division',
                                       'absolute_import', 'unicode_literals'])
        self.assertEqual(s,
                         ('from __future__ import '
                          '(absolute_import, division, print_function,\n'
                          '                        unicode_literals)'))

    def test_many(self):
        s = make_new_import_statement(['print_function', 'division',
                                       'absolute_import', 'unicode_literals',
                                       'nested_scopes', 'generators',
                                       'with_statement', 'more_keywords',
                                       'need_not_exist', 'lots_of_stuff'])
        self.assertEqual(s,
                         ('from __future__ import (absolute_import, division, '
                          'generators, lots_of_stuff,\n'
                          '                        more_keywords, '
                          'need_not_exist, nested_scopes,\n'
                          '                        print_function, '
                          'unicode_literals, with_statement)'))
