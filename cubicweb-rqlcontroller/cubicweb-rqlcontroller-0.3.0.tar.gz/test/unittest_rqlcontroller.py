# -*- coding: utf-8 -*-
# copyright 2013-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

import json
from cubicweb.devtools.httptest import CubicWebServerTC

try:
    # ensure a recent request lib is available
    import requests
    assert [int(n) for n in requests.__version__.split('.', 2)][:2] >= [1, 2]
except (ImportError, AssertionError):
    requests = None


class RqlIOTc(CubicWebServerTC):

    def setUp(self):
        "Skip whole test class if a suitable requests module is not available"
        if requests is None:
            self.skipTest('Python ``requests`` module is not available')
        super(RqlIOTc, self).setUp()
        req = self.request()
        self.create_user(req, u'toto', password=u'toto')

    def connectedRQLIOSession(self, login='admin', password='gingkow'):
        rsession = requests.Session()
        req = self.request()
        res = rsession.get('%s?__login=%s&__password=%s' % (
            req.base_url(), login, password))
        self.assertEqual(res.status_code, 200)
        return rsession

    def assertRQLPostOK(self, rsession, queries, code=200):
        req = self.request()
        res_ok = rsession.post(req.build_url('rqlio/1.0'),
                               data=json.dumps(queries),
                               headers={'Content-Type': 'application/json'})
        self.assertEqual(res_ok.status_code, code)
        return res_ok

    def assertRQLPostKO(self, rsession, queries, reason, code=500):
        req = self.request()
        res_ko = rsession.post(req.build_url('rqlio/1.0'),
                               data=json.dumps(queries),
                               headers={'Content-Type': 'application/json'})
        self.assertEqual(res_ko.status_code, code)
        self.assertIn(reason, res_ko.json()[u'reason'])
        return res_ko

    def test_queries(self):
        req = self.request()
        queries = [('INSERT CWUser U: U login %(l)s, U upassword %(p)s',
                    {'l': 'Babar', 'p': 'cubicweb rulez & 42'}),
                   ('INSERT CWGroup G: G name "pachyderms"', {}),
                   ('SET U in_group G WHERE U eid %(u)s, G eid %(g)s',
                    {'u': '__r0', 'g': '__r1'})]

        # as an anonymous user
        rsession = requests.Session()
        reason = (u'You are not allowed to perform add operation on relation'
                  ' CWUser in_group CWGroup')
        # should really be 403 if it wasn't for cubicweb brokenness
        self.assertRQLPostKO(rsession, queries, reason, code=500)

        # as a standard user
        rsession = self.connectedRQLIOSession('toto', 'toto')
        reason = (u'You are not allowed to perform add operation on relation'
                  ' CWUser in_group CWGroup')
        # should really be 403 if it wasn't for cubicweb brokenness
        self.assertRQLPostKO(rsession, queries, reason, code=500)

        # now, as an admin
        rsession = self.connectedRQLIOSession()
        res = self.assertRQLPostOK(rsession, queries)

        self.assertEqual('pachyderms',
                         self.execute('Any N WHERE U in_group G, U login "Babar", '
                                      'G name N').rows[0][0])
        output = [x for x, in res.json()]
        self.assertEqual(1, len(output[0]))
        self.assertEqual(1, len(output[1]))
        self.assertEqual(2, len(output[2]))
        self.assertEqual([output[0][0], output[1][0]], output[2])

    def test_rewrite_args_errors(self):
        rql1 = 'Any U WHERE U login %(l)s'
        rql2 = 'SET U in_group G WHERE G name "managers", U eid %(u)s'
        args2 = {'u': '__r0'}
        # setup test
        req = self.request()
        rsession = self.connectedRQLIOSession()
        # check ok
        queries_ok = [(rql1, {'l': 'toto'}), (rql2, args2)]
        self.assertRQLPostOK(rsession, queries_ok)
        # check ko (1)
        queries_ko = [(rql1, {'l': 'doesnotexist'}),
                      (rql2, args2)]
        self.assertRQLPostKO(rsession, queries_ko,
                       "__r0 references empty result set")
        # check ko (2)
        queries_ko = [('Any U WHERE U is CWUser', None),
                      (rql2, args2)]
        self.assertRQLPostKO(rsession, queries_ko,
                       "__r0 references multi lines result set")
        # check ko (3)
        queries_ko = [('Any U,L WHERE U login L, U login %(l)s',
                       {'l': 'toto'}), (rql2, args2)]
        self.assertRQLPostKO(rsession, queries_ko,
                       "__r0 references multi column result set")


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
