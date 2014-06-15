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

import mock

from qg.web.app import QFlaskApplication
from qg.db.app.exts import QDBAPIExtension


CONF = cfg.CONF


class FlaskApplication(QFlaskApplication):
    name = "test-app"
    version = "1.9"

    def create(self):
        super(FlaskApplication, self).create()
        self.register_extension(QDBAPIExtension())

    def init_flask_app(self):
        super(FlaskApplication, self).init_flask_app()

    def run(self):
        pass


class TestFlaskAppliation(TestCase):

    TESTDB_URI = 'sqlite:///:memory:'

    def test_db_init(self):

        CONF.set_default('connection', self.TESTDB_URI, 'database')
        app = FlaskApplication()
        with mock.patch('sys.argv', ['test', '--debug']):
            app.main()

        from qg.db.dbapi import get_dbapi
        from flask import current_app
        dbapi = get_dbapi()
        with app.flask_app.app_context():
            self.assertEqual(current_app.config['SQLALCHEMY_DATABASE_URI'],
                             self.TESTDB_URI)

            from sqlalchemy.orm.scoping import scoped_session
            self.assertTrue(isinstance(dbapi.session, scoped_session))

    def test_db_create_table(self):

        from qg.db import model_base
        import sqlalchemy as sa

        class SampleModel(model_base.BASE, model_base.HasIdMixin):

            hostname = sa.Column(sa.String(252), nullable=False, unique=True)
            lan_ip = sa.Column(sa.String(16), nullable=False, unique=True)

        CONF.set_default('connection', self.TESTDB_URI, 'database')
        app = FlaskApplication()
        with mock.patch('sys.argv', ['test', '--debug']):
            app.main()

        from qg.db.dbapi import get_dbapi
        with app.flask_app.app_context():
            get_dbapi().create_all()

            session = get_dbapi().session
            with session.begin(subtransactions=True):
                obj = SampleModel()
                obj.hostname = 'hostname'
                obj.lan_ip = '1.2.3.4'
                session.add(obj)

            retval = dict(session.query(SampleModel).one())
            self.assertEqual(retval['hostname'], obj.hostname)
            self.assertEqual(retval['lan_ip'], obj.lan_ip)
