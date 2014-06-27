# -*- coding: utf-8 -*-
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

"""cubicweb-searchui tests"""

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web import facet as facetbase

from cubes.searchui.views import RelationSwitchFacet


class RelationSwitchFacetTC(CubicWebTC):

    def build_relswitch_facet(self, rql, execute=False):
        req = self.request()
        if execute:
            rset = req.execute(rql)
            rqlst = rset.syntax_tree()
        else:
            rset = None
            rqlst = self.vreg.rqlhelper.parse(rql)
            self.vreg.solutions(req, rqlst, None) # compute solutions
        select = rqlst.children[0] # we need the SELECT node, not the UNION one
        filtered_variable = facetbase.get_filtered_variable(select)
        facetbase.prepare_select(select, filtered_variable)
        facet = facetbase.get_facet(req, 'relation-switch', select,
                                    filtered_variable=filtered_variable)
        facet.cw_rset = rset
        return facet


    def assertRelMapEqual(self, select, varname, expected):
        """
        Parameters:
            select: the Select statement to inspect
            varname: the pivot (selected) variable
            expected: a dictionary (rtype, pivot_role) -> target variable name
        """
        var = select.get_variable(varname)
        rels = RelationSwitchFacet.build_var_relmap(var, select)
        for k, v in rels.items():
            rels[k] = v.name
        self.assertDictEqual(rels, expected)

    def test_var_relmap(self):
        rqlst = self.vreg.rqlhelper.parse('Any U WHERE U is CWUser, '
                                          'U in_group G, G name "users", '
                                          'U in_state S, S state_of W')
        select = rqlst.children[0] # we need the SELECT node, not the UNION one
        self.assertRelMapEqual(select, 'U', {
            ('in_group', 'subject'): 'G',
            ('in_state', 'subject'): 'S',
        })
        self.assertRelMapEqual(select, 'G', {
            ('in_group', 'object'): 'U',
        })


    def test_possible_switches(self):
        facet = self.build_relswitch_facet('Any U WHERE U is CWUser, '
                                           'U in_group G, G name "users", '
                                           'U in_state S, S state_of W')
        self.assertEqual(facet.possible_switches(),
                         [('bookmarked_by', 'object', 'Bookmark'),
                          ('custom_workflow', 'subject', 'Workflow'),
                          ('for_user', 'object', 'CWProperty'),
                          ('in_group', 'subject', 'CWGroup'),
                          ('in_state', 'subject', 'State'),
                          ('primary_email', 'subject', 'EmailAddress'),
                          ('use_email', 'subject', 'EmailAddress'),
                          ('wf_info_for', 'object', 'TrInfo')])


    def test_possible_switches_with_skip_rtypes(self):
        facet = self.build_relswitch_facet('Any U WHERE U is CWUser, '
                                           'U in_group G, G name "users", '
                                           'U in_state S, S state_of W')
        facet.skip_rtypes = ('is_instance_of', 'is',
                             'bookmarked_by', 'custom_workflow',
                             'for_user', 'primary_email',
                             'wf_info_for')
        self.assertEqual(facet.possible_switches(),
                         [('in_group', 'subject', 'CWGroup'),
                          ('in_state', 'subject', 'State'),
                          ('use_email', 'subject', 'EmailAddress')])


    def test_switch_rql_queries(self):
        rql = ("Any U WHERE U is CWUser, U in_group G, G name 'users', "
               "U in_state S, S state_of W")
        facet = self.build_relswitch_facet(rql)
        base_restrictions = rql.split(' WHERE ')[1]
        rql_queries = [select.as_string()
                       for (_, _, _, select) in facet.switch_rql_queries()]
        expected_templates = ["DISTINCT Any A WHERE {base}, A bookmarked_by U, A is Bookmark",
                              "DISTINCT Any B WHERE {base}, U custom_workflow B, B is Workflow",
                              "DISTINCT Any C WHERE {base}, C for_user U, C is CWProperty",
                              "DISTINCT Any G WHERE {base}",
                              "DISTINCT Any S WHERE {base}",
                              "DISTINCT Any D WHERE {base}, U primary_email D, D is EmailAddress",
                              "DISTINCT Any E WHERE {base}, U use_email E, E is EmailAddress",
                              "DISTINCT Any F WHERE {base}, F wf_info_for U, F is TrInfo"]
        self.assertListEqual(rql_queries,
                             [tmpl.format(base=base_restrictions)
                              for tmpl in expected_templates])


    def test_vocabulary(self):
        rql = ("Any U WHERE U is CWUser, U in_group G, G name 'managers'")
        facet = self.build_relswitch_facet(rql, execute=True)
        base_restrictions = rql.split(' WHERE ')[1]
        self.assertListEqual(facet.vocabulary(),
                             [('in_group CWGroup',
                               'DISTINCT Any G WHERE {base}'.format(base=base_restrictions),
                               1),
                              ('in_state State',
                               'DISTINCT Any D WHERE {base}, U in_state D, D is State'.format(base=base_restrictions),
                               1)])

    def test_rqlpaths(self):
        facet = self.build_relswitch_facet('Any U WHERE U is CWUser')
        facet.rqlpaths = [('jump-to-workflow', ['X in_state S', 'S state_of W'], 'W')]
        facet.skip_rtypes = ('in_state',)
        values = [
            # in_group is computed by the standard relswitch loop
            (u'in_group CWGroup',
             'DISTINCT Any D WHERE U is CWUser, U in_group D, D is CWGroup',
             2),
            # in_state is computed by the rqlpath loop
            (u'jump-to-workflow',
             'DISTINCT Any I WHERE U is CWUser, U in_state H, H state_of I',
             1)]
        self.assertEqual(facet.vocabulary(), values)



if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
