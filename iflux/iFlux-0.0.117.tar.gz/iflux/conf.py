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

import importlib
import os
import sys
import ConfigParser

# Setting root path
ROOT = ''
if os.path.abspath(__file__).endswith('.py') or \
        os.path.abspath(__file__).endswith('.pyc'):
    ROOT = os.path.dirname(__file__)
else:
    ROOT = os.path.abspath(__file__)

# Getting configuration paths and files from the environment
try:
    IFLUX_CONFIG_FILE = os.environ['IFLUX_CONFIG_FILE']
except KeyError:
    IFLUX_CONFIG_FILE = 'iflux.ini'

# Setting config files

#Library file
LIB_CONFIG_FILE = os.path.join(sys.modules[__name__].ROOT, 'conf',
                               IFLUX_CONFIG_FILE)

# Application file
APP_CONFIG_ROOT_PATH = os.path.join(os.getcwd())
APP_CONFIG_PATH = os.path.join(APP_CONFIG_ROOT_PATH, 'conf')
APP_CONFIG_FILE = os.path.join(APP_CONFIG_PATH, 'iflux.ini')


# Setting template path
TEMPLATE_PATH = os.path.join(sys.modules[__name__].ROOT, 'templates')

stack = []

HAS_LIB_CONFIG_FILE = False
HAS_APP_CONFIG_FILE = False

if os.path.isfile(LIB_CONFIG_FILE):
    HAS_LIB_CONFIG_FILE = True
    stack.append(LIB_CONFIG_FILE)

if os.path.isfile(APP_CONFIG_FILE):
    HAS_APP_CONFIG_FILE = True
    stack.append(APP_CONFIG_FILE)

# Setting iflux default variables

# Application default configuration
application = dict()

application['data'] = dict()
application['data']['connections'] = dict()

application['port'] = 8888

# Data default configuration
data = dict()

data['connection'] = dict()
data['connection']['instances'] = dict()
data['connection']['handlers'] = dict()

# Data default configuration
modules = dict()

# Session default configuration
session = dict()
session['enabled'] = False
session['type'] = 'file'
session['handlers'] = dict()
session['path'] = ''
session['name'] = 'IFLUXSESSID'
session['redis_configuration'] = {
    'connection': 'session',
}
session['redis_prefix'] = 'iflux:session'
session['encoding'] = dict()
session['encoding']['type'] = 'pickle'
session['encoding']['encoders'] = dict()

# Static assets default variables
static_assets = dict()
static_assets_location = ''
static_assets_directory = \
    os.path.join(sys.modules[__name__].ROOT, 'static_assets')


# Used to parse the framework(system?) config file
def parse_config(config):

    if config.has_section('Data'):
        parse_data_section(config)

    if config.has_section('Modules'):
        parse_modules_section(config)

    if config.has_section('Session'):
        parse_session_section(config)

    if config.has_section('Static_Assets'):
        parse_static_assets_section(config)


# Used to parse the application config file
def parse_application_config(config):
    parse_config(config)
    parse_application_section(config)


def parse_application_section(config):
    if config.has_option('Application', 'port'):
        sys.modules[__name__].application['port'] = \
            config.getint('Application', 'port')

    if config.has_option('Application', 'data.connections'):
        sys.modules[__name__].application['data']['connections'] = \
            [x.strip(' ') for x in config.get('Application',
                                              'data.connections').split(',')]


def parse_data_section(config):
    data_items = config.items('Data')
    
    # We should accumulate the handlers and instances
    connection_instances = \
        sys.modules[__name__].data['connection']['instances']

    for key, value in data_items:
        key_x = key.split('.')
        if 'data.connection.instance' in key:
            instance_name = key_x[-2]
            if instance_name not in connection_instances:
                connection_instances[instance_name] = dict()
            connection_instances[instance_name][key_x[-1]] = value
        if 'data.connection.handler' in key:
            value_x = value.split('.')
            type = key_x[-1]
            sys.modules[__name__].data['connection']['handlers'][type] = dict()
            sys.modules[__name__].data['connection']['handlers'][type][
                'module'] = '.'.join(value_x[:-1][:])
            # TODO change the conf key from handler ro class
            sys.modules[__name__].data['connection']['handlers'][type][
                'handler'] = value_x[-1]
    for key in connection_instances:
        # TODO if type is not here send an error
        type = connection_instances[key]['type']
        # TODO Warn that case here or handle it better
        module = importlib.import_module(sys.modules[__name__].data[
            'connection']['handlers'][type]['module'])
        db_config = getattr(module, sys.modules[__name__].data[
            'connection']['handlers'][type]['handler']).parse_config(
            connection_instances[key])
        sys.modules[__name__].data['connection']['instances'][key] = db_config


def parse_modules_section(config):
    modules_items = config.items('Modules')
    for key, value in modules_items:
        if 'modules.' in key:
            key_x = key.split('.')
            if len(key_x) > 1:
                if key_x[1] not in sys.modules[__name__].modules:
                    sys.modules[__name__].modules[key_x[1]] = dict()
                    sys.modules[__name__].modules[key_x[1]]['enabled'] = False
                if len(key_x) == 2:
                    value_x = value.split('.')
                    sys.modules[__name__].modules[key_x[1]]['class'] = \
                        value_x[-1]
                    sys.modules[__name__].modules[key_x[1]]['module'] = \
                        '.'.join(value_x[:-1][:])
                elif len(key_x) == 3:
                    if key_x[-1] in ['enabled']:
                        sys.modules[__name__].modules[key_x[1]][key_x[-1]] = \
                            config.getboolean('Modules', key)
                    else:
                        sys.modules[__name__].modules[key_x[1]][key_x[-1]] = \
                            value


def parse_session_section(config):
    if config.has_option('Session', 'session.enabled'):
        sys.modules[__name__].session['enabled'] = \
            config.getboolean('Session', 'session.enabled')

    if config.has_option('Session', 'session.type'):
        sys.modules[__name__].session['type'] = \
            config.get('Session', 'session.type')

    if sys.modules[__name__].session['type'] == 'file':
        if config.has_option('Session', 'session.path'):
            sys.modules[__name__].session['path'] = \
                config.get('Session', 'session.path')

    if sys.modules[__name__].session['type'] == 'redis':
        if config.has_option('Session', 'session.redis.host'):
            sys.modules[__name__].session['redis_configuration']['host'] = \
                config.get('Session', 'session.redis.host')
        if config.has_option('Session', 'session.redis.port'):
            sys.modules[__name__].session['redis_configuration']['port'] = \
                config.getint('Session', 'session.redis.port')
        if config.has_option('Session', 'session.redis.port'):
            sys.modules[__name__].session['redis_configuration']['db'] = \
                config.getint('Session', 'session.redis.db')

    if config.has_option('Session', 'session.encoding.type'):
        sys.modules[__name__].session['encoding']['type'] = \
            config.get('Session', 'session.encoding.type')

    session_items = config.items('Session')
    for key, value in session_items:
        if 'session.handler' in key:
            value_x = value.split('.')
            type = key.split('.')[-1]
            sys.modules[__name__].session['handlers'][type] = dict()
            sys.modules[__name__].session['handlers'][type]['module'] = \
                '.'.join(value_x[:-1][:])
            sys.modules[__name__].session['handlers'][type]['class'] = \
                value_x[-1]
        if 'session.encoding.encoder' in key:
            value_x = value.split('.')
            type = key.split('.')[-1]
            sys.modules[__name__].session['encoding']['encoders'][
                type] = dict()
            sys.modules[__name__].session['encoding']['encoders'][
                type]['module'] = '.'.join(value_x[:-1][:])
            sys.modules[__name__].session['encoding']['encoders'][
                type]['class'] = value_x[-1]

def parse_static_assets_section(config):
    if config.has_option('Static_Assets', 'static_assets.location'):
        sys.modules[__name__].static_assets_location = \
            config.get('Static_Assets', 'static_assets.location')

    static_assets_items = config.items('Static_Assets')
    for key, value in static_assets_items:
        if 'version' in key:
            key_x = key.split('.')
            sys.modules[__name__].static_assets[key_x[2]] = dict()
            sys.modules[__name__].static_assets[key_x[2]][key_x[3]] = value
            sys.modules[__name__].static_assets[key_x[2]]['name'] = key_x[2]


# TODO: hardcoded! Maybe a constant!?
if os.path.isfile('/etc/iflux/iflux.ini'):
    HAS_OS_CONFIG_FILE = True
else:
    HAS_OS_CONFIG_FILE = False

if HAS_LIB_CONFIG_FILE:
    config = ConfigParser.ConfigParser()
    config.readfp(open(LIB_CONFIG_FILE))
    parse_config(config)

if HAS_APP_CONFIG_FILE:
    config = ConfigParser.ConfigParser()
    config.readfp(open(APP_CONFIG_FILE))
    parse_application_config(config)
