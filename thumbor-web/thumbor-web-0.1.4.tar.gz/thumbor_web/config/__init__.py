#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
from derpconf.config import Config, generate_config

MINUTE = 60
HOUR = 60 * MINUTE

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

Config.define('APP_SECRET_KEY', None, 'Secret key to configure application', 'Web')
Config.define('THUMBOR_SECURE_KEY', 'MY_SECURE_KEY', 'Thumbor Secret key', 'Web')
Config.define('THUMBOR_SERVER_URL', 'http://localhost:8888', 'Thumbor Secret key', 'Web')
Config.define('ASSETS_DIRECTORY', STATIC_PATH, 'Folder to be root directory for webassets', 'Web')
Config.define(
    'ASSETS_CACHE_DIRECTORY', os.path.join(STATIC_PATH, '.webassets_cache'),
    'Folder to be root directory for webassets cache', 'Web'
)
Config.define('ASSETS_AUTO_BUILD', True, 'Auto build static files', 'Web')
Config.define('ASSETS_SHOULD_CACHE', False, 'Cache static files', 'Web')

Config.define(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+mysqldb://root@localhost:3306/thumbor_web',
    'SQLAlchemy connection string to MySQL',
    'DB'
)


def init_app(app, path=None):
    conf = Config.load(path)
    for conf_option, _ in conf.items.items():
        app.config[conf_option] = conf[conf_option]

    app.secret_key = app.config['APP_SECRET_KEY']

if __name__ == '__main__':
    generate_config()
