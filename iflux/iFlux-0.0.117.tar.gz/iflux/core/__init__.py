# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
#
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

import ConfigParser
import iflux.conf
from iflux.core.data import configure_connection, DataConnectedMixin
from iflux.core.session import SessionEngineMixin
import importlib
import inspect
import os
import tornado.web


class Application(tornado.web.Application, DataConnectedMixin,
                  SessionEngineMixin):

    session = None

    modules = {} 

    def __init__(self, informed_handlers=[], **settings):
        configure_connection(iflux.conf.application['data']['connections'], self)
        static_handlers = [
            (r"/static_assets/(.*)", tornado.web.StaticFileHandler,
             {"path": iflux.conf.static_assets_directory}),
        ]

        if 'iflux_template_path' not in settings:
            settings['iflux_template_path'] = iflux.conf.TEMPLATE_PATH

        # TODO: Make shure they don't specify reserved handlers here
        handlers = informed_handlers + static_handlers
        
        self.__load_modules()

        for key, module in self.modules.iteritems():
            module_handlers = module.get_handlers()
            for i in range(0, len(module_handlers)):
                if len(module_handlers[i]) < 3:
                    module_handlers[i] = (module_handlers[i][0],
                                          module_handlers[i][1],
                                          {'application_module': module})
            handlers = handlers + module_handlers
        tornado.web.Application.__init__(self, handlers, **settings) 

    def __load_modules(self):
        for key, value in iflux.conf.modules.iteritems():
            if value['enabled']:
                module_module = importlib.import_module(value['module'])
                module_class = getattr(module_module, value['class'])
                self.modules[key] = module_class(key, self)
                module_config_file = os.path.join(
                    iflux.conf.APP_CONFIG_PATH,
                    self.modules[key].get_config_file())
                config = ConfigParser.ConfigParser()
                if os.path.isfile(module_config_file):
                    config.readfp(open(os.path.join(module_config_file)))
                self.modules[key].process_config(config)


class ApplicationModule(object):


    def __init__(self, name, application):
        self.name = name
        self.application = application
        self.configuration = dict()

    def get_handlers(self):
        return []

    def get_module_path(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def get_template_path(self):
        return self.__build_template_path()

    def __build_template_path(self):
        return os.path.join(os.path.dirname(
            inspect.getfile(self.__class__)), 'templates')

    def get_config_file(self):
        return 'iflux.ini'

    def process_config(self, config):
        pass

    def pre_install(self):
        pass

    def install(self):
        pass

    def post_install(self):
        pass
