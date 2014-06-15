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

from qg.core.app import QExtension
from qg.core.exception import QException
from qg.web.app.flaskapp import QFlaskApplication

import qg.db.dbapi

# NOTE(jianingy): 以后可能会同时用到多个库。如果遇到这种需求，就用oslo.config传
# 入一个 dict 用来保存每个库的 URI 。这事 --database-connection 就可以当做 default
# 这个库的 URI 来用了。

database_opts = [
    cfg.StrOpt('connection',
               default='sqlite:///rssboard.db',
               help='The database connection string'),
]

CONF = cfg.CONF
CONF.register_cli_opts(database_opts, 'database')
CONF.register_opts(database_opts, 'database')


class ApplicationTypeError(QException):
    message = "FlaskDBAPI requires FlaskApplication."


class QDBAPIExtension(QExtension):

    name = 'dbapi'
    session_options = {
        'autocommit': True
    }

    def post_init_app(self, evt, app, retval):
        if not isinstance(app, QFlaskApplication):
            raise ApplicationTypeError()

        qg.db.dbapi._DBAPI.init_app(app.flask_app)

    def post_configure(self, evt, app, retval):
        flask_app = app.flask_app
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = CONF.database.connection
