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
from qg.core.gettextutils import _
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy import text

import six

from treestore.db.api import model_query, get_session
from treestore.models.tree_node import TreeNode
from treestore.exceptions import InvalidValue, NodeNotFound, InvalidQuery


def get_node(path):
    try:
        node_query = model_query(TreeNode).filter(
            TreeNode.canonical_path == path)
        return node_query.one()
    except orm_exc.NoResultFound:
        raise NodeNotFound(path=path)


def get_descendants(path):
    unbind = text('canonical_path <@ :path')
    bound = unbind.bindparams(path=path)
    node_query = model_query(TreeNode).filter(bound)
    return node_query.all()


def search_by_path(lquery):
    try:
        unbind = text('canonical_path ~ :lquery')
        bound = unbind.bindparams(lquery=lquery)
        node_query = model_query(TreeNode).filter(bound)
        return node_query.all()
    except sa_exc.ProgrammingError:
        raise InvalidQuery(query=lquery)


def search_by_values(**kwargs):
    try:
        node_query = model_query(TreeNode)
        for key, value in six.iteritems(kwargs):
            node_query = node_query.filter(TreeNode.values[key] == value)
        return node_query.all()
    except sa_exc.ProgrammingError:
        raise InvalidQuery(query=str(kwargs))


def create_node(path, values):
    if not isinstance(values, dict):
        raise InvalidValue(reason=_("Value must be a dict"))
    session = get_session()
    with session.begin(subtransactions=True):
        node = TreeNode(canonical_path=path, values=values)
        session.add(node)


def delete_node(path):
    node_query = model_query(TreeNode).filter(TreeNode.canonical_path == path)
    node_query.delete()
