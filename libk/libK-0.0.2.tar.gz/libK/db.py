from kernel import kernel
import MySQLdb

__author__ = 'negash'


class MySQL:
    mysql = {}
    data_kernel_db = {}
    cursor = {}

    # create connection vars
    def __init__(self, dbs):
        self.data_kernel_db = dbs
        for i in self.data_kernel_db.keys():
            self.mysql[i] = ''

    # simple query to db
    def q(self, database, query, params=None):
        # create connect if is null
        if self.mysql[database] == '':
            self.mysql[database] = MySQLdb.connect(host=self.data_kernel_db[database]['host'],
                                                   user=self.data_kernel_db[database]['user'],
                                                   passwd=self.data_kernel_db[database]['passwd'],
                                                   db=self.data_kernel_db[database]['db'])
            self.cursor[database] = self.mysql[database].cursor()
        # run query and return
        return self.cursor[database].execute(query, params)

    # return result
    def af(self, database):
        return self.cursor[database].fetchall()

    # return result in array
    def s(self, database, query, params=None):
        # query
        db.q(database, query, params)
        # columns in result
        columns = self.cursor[database].description
        result = []
        # create array with key => result
        for value in db.af(database):
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        return result

    # get current result for all rows
    def sc(self, database, query, params=None):
        db.q(database, query, params)
        result = []
        for value in db.af(database):
            for (index, column) in enumerate(value):
                result.append(column)
        return result

    # select one row
    def s1(self, database, query, params=None):
        db.q(database, query, params)
        columns = self.cursor[database].description
        tmp = {}
        for value in db.af(database):
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            break
        return tmp

    # close all connections
    def c(self):
        for i in self.data_kernel_db.keys():
            self.cursor[i].close()
            self.cursor[i] = ''
            self.mysql[i] = ''


db = MySQL(kernel['db'])