# -*- coding: utf-8 -*-

#    Copyright (C) 2014 AT&T Labs All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib

import testtools
from zake import fake_client

from taskflow.openstack.common import uuidutils
from taskflow.persistence import backends
from taskflow.persistence.backends import impl_zookeeper
from taskflow import test
from taskflow.tests.unit.persistence import base
from taskflow.tests import utils as test_utils

TEST_PATH_TPL = '/taskflow/persistence-test/%s'
_ZOOKEEPER_AVAILABLE = test_utils.zookeeper_available(
    impl_zookeeper.MIN_ZK_VERSION)


@testtools.skipIf(not _ZOOKEEPER_AVAILABLE, 'zookeeper is not available')
class ZkPersistenceTest(test.TestCase, base.PersistenceTestMixin):
    def _get_connection(self):
        return self.backend.get_connection()

    def _clear_all(self):
        with contextlib.closing(self._get_connection()) as conn:
            conn.clear_all()

    def setUp(self):
        super(ZkPersistenceTest, self).setUp()
        conf = test_utils.ZK_TEST_CONFIG.copy()
        # Create a unique path just for this test (so that we don't overwrite
        # what other tests are doing).
        conf['path'] = TEST_PATH_TPL % (uuidutils.generate_uuid())
        try:
            self.backend = impl_zookeeper.ZkBackend(conf)
            self.addCleanup(self.backend.close)
        except Exception as e:
            self.skipTest("Failed creating backend created from configuration"
                          " %s due to %s" % (conf, e))
        with contextlib.closing(self._get_connection()) as conn:
            conn.upgrade()
            self.addCleanup(self._clear_all)

    def test_zk_persistence_entry_point(self):
        conf = {'connection': 'zookeeper:'}
        with contextlib.closing(backends.fetch(conf)) as be:
            self.assertIsInstance(be, impl_zookeeper.ZkBackend)


@testtools.skipIf(_ZOOKEEPER_AVAILABLE, 'zookeeper is available')
class ZakePersistenceTest(test.TestCase, base.PersistenceTestMixin):
    def _get_connection(self):
        return self._backend.get_connection()

    def setUp(self):
        super(ZakePersistenceTest, self).setUp()
        conf = {
            "path": "/taskflow",
        }
        self.client = fake_client.FakeClient()
        self.client.start()
        self._backend = impl_zookeeper.ZkBackend(conf, client=self.client)
        conn = self._backend.get_connection()
        conn.upgrade()

    def test_zk_persistence_entry_point(self):
        conf = {'connection': 'zookeeper:'}
        with contextlib.closing(backends.fetch(conf)) as be:
            self.assertIsInstance(be, impl_zookeeper.ZkBackend)
