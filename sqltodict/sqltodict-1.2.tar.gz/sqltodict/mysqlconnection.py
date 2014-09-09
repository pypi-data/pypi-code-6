# -*- coding: utf-8 -*-

import mysql.connector
from .baseconnection import BaseConnection
from .exceptions import MySqlConnectionError, NoneCursorError

class MYSQLConnection(BaseConnection):

    def make_connection(self):
        """ Basicly to build mysql connection by given attributes """
        try:
            self.connection=mysql.connector.connect(database=self.dbname,
                                                    user=self.user,
                                                    password=self.password,
                                                    host=self.host,
                                                    port=self.port)
        except Exception, e:
            raise MySqlConnectionError, e

    def get_columns(self):
        """ MYSQL description holding style as 
            list so as the action based on that """
        try:
            return map(lambda x: x[0], self.cursor.description)
        except AttributeError,e:
            raise NoneCursorError, e
