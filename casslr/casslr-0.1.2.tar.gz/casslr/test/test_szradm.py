# coding:utf-8
import os

from casslr.lib.szradm import FarmRoleNotFound
from casslr.test.util import FarmRoleEngineTestCase


class FindRoleTestCase(FarmRoleEngineTestCase):
    def setUp(self):
        super(FindRoleTestCase, self).setUp()
        with open(os.path.join(self.test_data, "roles-valid.xml")) as f:
            self.engine.responses = [f.read()]

    def test_find_farm_role(self):
        id = 67453

        role = self.engine.farm_role_by_id(id)

        self.assertEqual(id, role.id)
        self.assertEqual(2, len(role.servers))

        s0, s1 = role.servers

        self.assertEqual(1, s0.index)
        self.assertEqual(2, s1.index)

        self.assertEqual("54.81.242.68", s0.external_ip)
        self.assertEqual("10.184.45.97", s1.internal_ip)

    def test_find_farm_role_other(self):
        self.assertEqual(1, len(self.engine.farm_role_by_id(67455).servers))

    def test_no_farm_role(self):
        self.assertRaises(FarmRoleNotFound, self.engine.farm_role_by_id, 99999)


class UserDataTestCase(FarmRoleEngineTestCase):
    def setUp(self):
        super(UserDataTestCase, self).setUp()
        with open(os.path.join(self.test_data, "user-data.xml")) as f:
            self.engine.responses = [f.read()]

    def test_farm_role_id(self):
        self.assertEqual(123, self.engine.current_farm_role_id())
