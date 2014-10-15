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

import sys


class ConnectionHandler(object):

    data_connected_instance = None

    def __init__(self, data_connected_instance):
        self.data_connected_instance = data_connected_instance


class RedisDataConnectionHandler(ConnectionHandler):

    connection = None
 
    def configure(self, config):
        import redis
        redis_config = dict()
        redis_config.update(config)
        redis_config.pop("type")
        # TODO Handle connection error
        self.connection = redis.Redis(**redis_config)

    def get_connection(self):
        return self.connection

    @staticmethod
    def parse_config(config):
        db_config = {
            'type': 'redis',
            'host': 'localhost',
            'port': 6379,
            'db': 0,
        }
        for key in config:
            if key in ['db', 'host', 'port']:
                if key in ['db', 'port']:
                    db_config[key] = int(config[key])
                db_config[key] = config[key]
        return db_config


class SqlalchemyDataConnectionHandler(ConnectionHandler):
    
    __connection = {
        'engine': None,
        'session': None,
    }
   
    def configure(self, config):
        from sqlalchemy import create_engine
        from sqlalchemy.exc import OperationalError
        from iflux.util.sqlalchemy_util import Session

        self.__connection['engine'] = create_engine(config['url'])
        try:
            self.__connection['engine'].connect()
        except OperationalError as error:
            sys.exit("Error connecting to the database: " + error.message)

        Session.configure(bind=self.__connection['engine'])
        self.__connection['session'] = Session()
        # TODO: Test the session right here. Without that the error 
        # will just happen during the handler execution

    def get_connection(self):
        return self.__connection

    @property
    def engine(self):
        return self.__connection['engine']

    @property
    def session(self):
        return self.__connection['session']

    @staticmethod
    def parse_config(config):
        db_config = {
            'type': 'sqlalchemy',
        }
        for key in config:
            # TODO Need to handle other properies and create the url if needed.
            if key in ['url']:
                db_config[key] = config[key]
        return db_config
