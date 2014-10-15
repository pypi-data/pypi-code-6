# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from iflux.modules.admin.handlers import DashboardHandler
from iflux.core import ApplicationModule
import tornado.web
import os

class AdminModule(ApplicationModule):

    current_instance = None

    table_prefix = 'admin'
    connection_instance = 'admin'

    def get_handlers(self):
        handlers = [
            (r'/admin', DashboardHandler),
            (r"/admin/static/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_module_path(), 'static')}),
        ]
        return handlers

    def get_config_file(self):
        return "admin.ini"

    def process_config(self, config):
        if config.has_option('Admin', 'admin.table.prefix'):
            self.table_prefix = config.get('Admin', 'admin.table.prefix')
        if config.has_option('Admin', 'admin.data.connection.instance'):
            self.connection_instance = config.get('Admin',
                'admin.data.connection.instance'
            )
        AdminModule.current_instance = self

    def install(self):
        print "installing"
        import iflux.modules.admin.models
        from iflux.util.sqlalchemy_util import Base

        table_prefix = self.table_prefix
        engine = self.__get_connection_handler().get_connection()['engine']
        engine.echo=True
        # Dropping all
        Base.metadata.drop_all(engine)
        # Creating database
        Base.metadata.create_all(engine)

    def __get_connection_handler(self):
        return self.application.get_connection_handler(
            self.connection_instance
        )
