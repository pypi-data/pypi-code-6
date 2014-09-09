# -*- coding: utf-8 -*-

import psycopg2
from .baseconnection import BaseConnection
from .exceptions import PostgreSQLConnectionError, NoneCursorError

class PostgreSQLConnection(BaseConnection):

    def make_connection(self):
        """ Basicly to build postgres connection by given attributes """
        try:
            self.connection=psycopg2.connect(database=self.dbname,
                                             user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port)
        except Exception, e:
            raise PostgreSQLConnectionError, e

    def get_columns(self):
        """ PostgreSQL description holding style as
            list so as the action based on that """
        try:
            return map(lambda x: x.name, self.cursor.description)
        except AttributeError,e:
            raise NoneCursorError, e
