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

from cubicweb.devtools.testlib import CubicWebTC

from cubes.container.testutils import ContainerMixinTC


class OwnedByHookTC(ContainerMixinTC, CubicWebTC):

    def setup_database(self):
        self.create_user(self.request(), 'u')
        self.commit()
        with self.login('u'):
            req = self.request()
            self.eid = req.create_entity('CollaborativeEntity').eid
            self.commit()

    def logins_with_perm_on(self, perm, eid, req=None):
        """Logins of users with `perm` permisssion on entity with `eid`"""
        req = req or self.request()
        return [u.login for u in req.entity_from_eid(eid).related(
            'can_' + perm, role='object', entities=True)]

    def test_creator(self):
        """Creator can read/write her entity"""
        self.assertEqual(['u'], self.logins_with_perm_on('read', self.eid))
        self.assertEqual(['u'], self.logins_with_perm_on('write', self.eid))

    def test_owners(self):
        """Add/remove an owner, check read/write permissions get updated"""
        req = self.request()
        user2 = self.create_user(req, 'v')
        self.commit()
        req.execute('SET X owned_by U WHERE U login "v", X eid %d' % self.eid)
        self.commit()
        self.assertEqual(['u', 'v'],
                         self.logins_with_perm_on('read', self.eid))
        self.assertEqual(['u', 'v'],
                         self.logins_with_perm_on('write', self.eid))
        req.execute('DELETE X owned_by U WHERE U login "v", X eid %d' % self.eid)
        self.commit()
        self.assertEqual(['u'], self.logins_with_perm_on('read', self.eid))
        self.assertEqual(['u'], self.logins_with_perm_on('write', self.eid))


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
