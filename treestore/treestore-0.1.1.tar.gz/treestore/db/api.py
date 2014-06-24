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

from qg.db import api as db_api
from qg.db import models


def get_session(*args, **kwargs):
    return db_api.get_session(*args, **kwargs)


def get_engine(*args, **kwargs):
    return db_api.get_engine(*args, **kwargs)


def model_query(model, session=None, args=None, **kwargs):
    """Query helper for db.sqlalchemy api methods without openstack
       specific arguments.

    This accounts for `deleted` and `project_id` fields.

    :param model:        Model to query. Must be a subclass of ModelBase.
    :type model:         models.ModelBase

    :param session:      The session to use.
    :type session:       sqlalchemy.orm.session.Session

    :param args:         Arguments to query. If None - model is used.
    :type args:          tuple

    Usage:

    .. code-block:: python


      def get_instance_by_uuid(uuid):
          session = get_session()
          with session.begin()
              return (utils.model_query(models.Instance, session=session)
                           .filter(models.Instance.uuid == uuid)
                           .first())

      def get_nodes_stat():
          data = (Node.id, Node.cpu, Node.ram, Node.hdd)

          session = get_session()
          with session.begin()
              return utils.model_query(Node, session=session, args=data).all()

    """

    if not issubclass(model, models.ModelBase):
        raise TypeError(_("model should be a subclass of ModelBase"))

    if not session:
        session = get_session()
    query = session.query(model) if not args else session.query(*args)

    return query
