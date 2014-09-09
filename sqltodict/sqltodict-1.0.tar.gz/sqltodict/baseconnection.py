# -*- coding: utf-8 -*-

from .exceptions import ExecutionError, GenerationDictError

class BaseConnection(object):
    def __init__(self, sql, dbname=None, user=None, host=None,
                 password=None, port=None, cursor=None):
        self.sql=sql
        self.dbname=dbname
        self.user=user
        self.host=host
        self.password=password
        self.port=port
        self.cursor=cursor
        self.connection=None
        self.result=None

    @classmethod
    def cursorready(cls, sql, cursor):
        """
        Connection can be established already,
        so the class can also be generated
        """
        return cls(sql=sql, cursor=cursor)

    def make_connection(self):
        """ Each server connection is different from eachother """
        pass

    def get_columns(self):
        """ Each server has differences for how
            to hold description of an cursor.
        """
        pass

    def execute_sql(self):
        """ To execute raw sql """
        try:
            if not self.cursor:
                self.make_connection()
                self.cursor=self.connection.cursor()
            self.cursor.execute(self.sql)
            self.result=self.cursor.fetchall()
        except Exception, e:
            raise ExecutionError, e

    def execute_return_as_dict(self):
        """ Generation dictionary from the result """
        self.execute_sql()
        data=self.result
        try:
            columns = self.get_columns()
            data=[dict(zip(columns, row)) for row in self.result]
        except Exception, e:
            raise GenerationDictError, e
        return data
