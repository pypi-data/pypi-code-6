# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-collaboration tests of utilities"""

from unittest import TestCase

from yams.buildobjs import EntityType, RelationDefinition
from yams.reader import build_schema_from_namespace

from cubicweb.schema import ERQLExpression, RRQLExpression

# Import "extended" EntityType and RelationDefinition classes.
import cubes.collaboration


class SchemaPermissionsTC(TestCase):
    """Test cases for schema classes permissions extension utilities"""

    def setUp(self):
        class Clown(EntityType):
            __permissions__ = {
                'read':   ('managers', ERQLExpression('X title N'),
                           ERQLExpression('X sad True')),
                'add':    ('managers', 'users'),
                'update': ('managers',),
                'delete': ('managers', 'owners'),
                }

        class Joke(EntityType):
            """Funny"""

        class tricks(RelationDefinition):
            __permissions__ = {
                'read': ('managers', 'users', 'guests'),
                'add': ('managers', 'users'),
                'delete': ('managers', RRQLExpression('S title N'),
                           RRQLExpression('O funny True'))
            }
            subject = 'Clown'
            object  = 'Joke'

        self.schema = build_schema_from_namespace(locals().items())

    def test_redundant_variable(self):
        etype = self.schema['Clown']
        with self.assertRaises(Exception) as cm:
            etype.permissions_add_mandatory_rqlexpression('read', 'X color N')
        self.assertEqual(str(cm.exception),
                         'Variable `N` already used in RQL expression '
                         '`X title N`')

    def test_etype_add_mandatory_rqlexpr(self):
        etype = self.schema['Clown']
        etype.permissions_add_mandatory_rqlexpression(
            'read', 'X color V, V is "red"')
        self.assertEqual(etype.permissions['read'],
                         ('managers',
                          ERQLExpression('X color V, V is "red", X title N'),
                          ERQLExpression('X color V, V is "red", X sad True')))

    def test_etype_add_mandatory_rqlexpr_no_rqlexpr_yet(self):
        etype = self.schema['Clown']
        etype.permissions_add_mandatory_rqlexpression('add', 'X color V')
        self.assertEqual(etype.permissions['add'],
                         ('managers', 'users', ERQLExpression("X color V")))

    def test_etype_set_permissions_groups(self):
        etype = self.schema['Clown']
        etype.set_permissions_groups('read', ('clowns', 'monkeys'))
        self.assertEqual(etype.permissions['read'],
                         ('clowns', 'monkeys', ERQLExpression('X title N'),
                          ERQLExpression('X sad True')))

    def test_rdef_add_mandatory_rqlexpr(self):
        rdef = self.schema['tricks'].rdefs['Clown', 'Joke']
        rdef.permissions_add_mandatory_rqlexpression(
            'delete', 'S name "bozo"')
        self.assertEqual(rdef.permissions['delete'],
                         ('managers',
                          RRQLExpression('S name "bozo", S title N'),
                          RRQLExpression('S name "bozo", O funny True')))

    def test_rdef_add_mandatory_rqlexpr_no_rqlexpr_yet(self):
        rdef = self.schema['tricks'].rdefs['Clown', 'Joke']
        rdef.permissions_add_mandatory_rqlexpression('add', 'S color V')
        self.assertEqual(rdef.permissions['add'][-1],
                         RRQLExpression("S color V"),)

    def test_rdef_set_permissions_groups(self):
        rdef = self.schema['tricks'].rdefs['Clown', 'Joke']
        rdef.set_permissions_groups('read', ('clowns', 'monkeys'))
        self.assertEqual(rdef.permissions['read'],
                         ('clowns', 'monkeys'))


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
