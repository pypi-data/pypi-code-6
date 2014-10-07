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

from cubicweb.devtools import testlib
from cubicweb import NoSelectableObject
from cubicweb.web import Redirect

class MassMailingTC(testlib.CubicWebTC):

    def actions(self, req, rset):
        actions = self.vreg['actions'].poss_visible_objects(req, rset=rset)
        return set(action.__regid__ for action in actions)


    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.execute('INSERT EmailAddress X: X address L + "@cubicweb.org", '
                        'U use_email X WHERE U is CWUser, U login L')
            cnx.commit()


    def test_action_sendmail_admin(self):
        with self.admin_access.web_request() as req:
            self.assertIn('sendemail', self.actions(req, req.execute('CWUser X')))

    def test_action_sendmail_anon(self):
        with self.new_access('anon').web_request() as req:
            self.assertNotIn('sendemail', self.actions(req, req.execute('CWUser X')))

    def test_form(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('CWUser X')
            form = self.vreg['forms'].select('massmailing', req, rset)
            self.assertEqual(['creation_date', 'cwuri', 'eid', 'firstname',
                          'last_login_time', 'login', 'modification_date',
                          'surname'],
                         form.get_allowed_substitutions())

    def test_view(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('CWUser X')
            # simply test the view is correct (x)HTML
            self.view('massmailing', rset, template=None)

    def test_controller_missing_params(self):
        with self.admin_access.web_request() as req:
            self.assertRaises(NoSelectableObject, self.vreg['controllers'].select,
                              'sendmail', req)

    def test_controller_anon(self):
        with self.new_access('anon').web_request() as req:
            self.assertRaises(NoSelectableObject,
                              self.vreg['controllers'].select, 'sendmail', req)

    def test_controller_admin(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.user.cw_set(firstname=u'Sÿt', surname=u'Thénault')
            cnx.commit()
            rset = cnx.execute('CWUser X')
        with self.admin_access.web_request(subject='tôtô', sender=u'S. Thénô <stheno@dactylo.fr>',
                               recipient=[str(eid) for eid, in rset],
                               mailbody='hôp %(firstname)s %(surname)s') as req:
            ctrl = self.vreg['controllers'].select('sendmail', req)
            with self.assertRaises(Redirect) as cm:
                ctrl.publish()
            url = cm.exception.location
            self.assertTrue(url.startswith('http://testing.fr/cubicweb/view?_cwmsgid='))
            self.assertEqual(len(testlib.MAILBOX), len(rset))
            email = [mail for mail in testlib.MAILBOX
                     if mail.recipients == ['admin@cubicweb.org']][0]
            self.assertEqual(u'hôp Sÿt Thénault', email.content)
            self.assertEqual(u'tôtô', email.subject)
            self.assertEqual(u'S. Thénô <stheno@dactylo.fr>', email.fromaddr)
            self.assertEqual(u'S. Thénô <stheno@dactylo.fr>', email.message['From'])


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
