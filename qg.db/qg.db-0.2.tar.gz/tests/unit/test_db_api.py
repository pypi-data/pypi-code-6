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
from oslo.config import cfg
from testtools import TestCase
from sqlalchemy.ext.declarative import declarative_base

from oslo.db import options
from qg.db import models
from qg.db.api import get_engine, get_session

CONF = cfg.CONF
BASE = declarative_base(cls=models.ModelBase)

CONF.register_opts(options.database_opts, 'database')


class TestDBAPI(TestCase):

    TESTDB_URI = 'sqlite://'

    def test_db_init(self):
        from sqlalchemy.orm.session import Session
        CONF.set_default('connection', self.TESTDB_URI, 'database')
        self.assertIsInstance(get_session(), Session)

    def test_db_create_table(self):

        import sqlalchemy as sa

        class SampleModel(BASE, models.TableNameMixin, models.HasIdMixin):

            hostname = sa.Column(sa.String(252), nullable=False, unique=True)
            lan_ip = sa.Column(sa.String(16), nullable=False, unique=True)

        CONF.set_default('connection', self.TESTDB_URI, 'database')
        BASE.metadata.create_all(get_engine())
        session = get_session()
        with session.begin(subtransactions=True):
            obj = SampleModel()
            obj.hostname = 'hostname'
            obj.lan_ip = '1.2.3.4'
            session.add(obj)

        retval = dict(session.query(SampleModel).one())
        self.assertEqual(retval['hostname'], obj.hostname)
        self.assertEqual(retval['lan_ip'], obj.lan_ip)
