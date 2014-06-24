# -*- coding: utf-8 -*-
#
# Copyright 2014, Qunar OPSDEV
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Author: Jianing Yang <jianingy.yang@gmail.com>
#

from fixture import DataSet, SQLAlchemyFixture
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase

import fixtures

from treestore.db.api import get_engine
from treestore.exceptions import NodeNotFound, InvalidQuery
from treestore.models.tree_node import TreeNode
from treestore.services import node as node_service

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class TreeNodeData(DataSet):

    class com_example_corp:
        canonical_path = 'com.example.corp'
        values = {'num_servers': '511', 'site': 'corp'}

    class com_example_cn2:
        canonical_path = 'com.example.cn2'
        values = {'site': 'cn2'}

    class com_example_cn2_search1:
        canonical_path = 'com.example.cn2.search1'
        values = {'site': 'cn2', 'host': 'yes'}

    class com_example_disabled:
        canonical_path = 'com.example.disabled'
        values = {}


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(engine=get_engine(),
                                           env={'TreeNodeData': TreeNode})
        self.data = self.dbfixture.data(TreeNodeData)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_node(self):
        node = node_service.get_node('com.example.corp')
        self.assertIsInstance(node, TreeNode)
        self.assertEqual(node.values['num_servers'], '511')

    def test_get_missing_node(self):
        self.assertRaises(NodeNotFound, node_service.get_node, 'a.b.c')

    def test_get_descendants(self):
        nodes = node_service.get_descendants('com.example.cn2')
        paths = map(lambda x: x.canonical_path, nodes)
        self.assertEqual(len(paths), 2)

    def test_search_by_path(self):
        nodes = node_service.search_by_path('com.example.*{1}')
        paths = map(lambda x: x.canonical_path, nodes)
        self.assertEqual(len(paths), 3)

    def test_search_by_values(self):
        nodes = node_service.search_by_values(site='cn2')
        paths = map(lambda x: x.canonical_path, nodes)
        self.assertEqual(len(paths), 2)

    def test_search_by_values_multi_cond(self):
        nodes = node_service.search_by_values(site='cn2', host='yes')
        paths = map(lambda x: x.canonical_path, nodes)
        self.assertEqual(len(paths), 1)

    def test_search_by_path_invalid_query(self):
        self.assertRaises(InvalidQuery, node_service.search_by_path, '.....')

    def test_create_node_with_empty_value(self):
        node_service.create_node('com.example.new', {}),
        self.assertIsInstance(node_service.get_node('com.example.new'),
                              TreeNode)
        node_service.delete_node('com.example.new')

    def test_create_node_with_value(self):
        node_service.create_node('com.example.new', {"num_servers": '128'}),
        self.assertIsInstance(node_service.get_node('com.example.new'),
                              TreeNode)
        node_service.delete_node('com.example.new')

    def test_delete_node(self):
        node_service.delete_node('com.example.disabled')
        self.assertRaises(NodeNotFound,
                          node_service.get_node,
                          'com.example.disabled')

    def test_delete_missing_node(self):
        node_service.delete_node('a.b.c')
