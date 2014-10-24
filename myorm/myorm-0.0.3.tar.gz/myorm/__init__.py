#!/usr/bin/env python
# coding: utf-8

AUTHOR = "Christian Kokoska"

from flask import g

class InvalidFieldName(Exception):
    pass

class NoParameters(Exception):
    pass

class DbObject(object):
    """
    The main model which provides the ORM
    """
    def __init__(self):
        self.adaptor = None

    @classmethod
    def all(cls):
        return [cls(*item) for item in cls.adaptor.get_all(cls.tablename,
                                                           cls.fieldnames)]

    @classmethod
    def ordered(cls, criteria=None, direction='ASC'):
        return [cls(*item) for item in cls.adaptor.get_ordered(criteria,
                                                               direction,
                                                               cls.tablename,
                                                               cls.fieldnames)]

    @classmethod
    def get(cls, *args, **kwargs):
        if not kwargs:
            raise NoParameters('No parameters provided')
        return cls.filter(*args, **kwargs)[0]

    @classmethod
    def filter(cls, *args, **kwargs):

        if not kwargs:
            raise NoParameters('No parameters provided')

        filters = []

        for key, value in kwargs.iteritems():
            filters.append("%s='%s'" % (key, value))
        filter = (' and ').join(filters)

        return [cls(*item) for item in cls.adaptor.get_by_filter(
                                                                filter,
                                                                cls.tablename,
                                                                cls.fieldnames)]

    @classmethod
    def create(cls, *args, **kwargs):
        return cls.adaptor.create(cls, cls.tablename, cls.fieldnames, kwargs)

    def save(self, *args, **kwargs):
        if self.id:
            self.update(self.tablename, self.fieldnames, kwargs)
        else:
            for fieldname in self.fieldnames:
                kwargs[fieldname] = getattr(self, fieldname)
            self.create(self, self.tablename, self.fieldnames, **kwargs)

    def update(self, *args, **kwargs):
        return self.adaptor.update(self.tablename, self.fieldnames, self)


class Adaptor():

    def update(self, tablename, fieldnames, *args):
        _object = args[0]
        settings = ""
        for fieldname in fieldnames:
            settings += ", " + fieldname + "=%s"
        settings = settings[2:]

        query = "UPDATE %s SET %s WHERE id = %%s" % (tablename, settings)

        values = []
        for fieldname in fieldnames:
            values.append(getattr(_object, fieldname))
        values.append(_object.id)

        con = self.get_connection()
        con.cursor().execute(query, values)
        con.commit()


class PostgreSQLAdaptor(Adaptor):

    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    def get_connection(self):
        import psycopg2
        con = psycopg2.connect(host=self.host,
                              database=self.database,
                              user=self.username,
                              password=self.password)
        return con


    def get_by_sql(self, query, *args):
        cur = self.get_connection().cursor()
        cur.execute(query)
        return cur.fetchall()

    def get_by_filter(self, filter, *args):
        tablename = args[0]
        fieldnames = args[1]
        query = "SELECT %s FROM %s WHERE %s" % (', '.join(fieldnames),
                                                tablename,
                                                filter)
        return self.get_by_sql(query, *args)

    def get_all(cls, *args):
        return cls.get_by_filter("1 = 1", *args)

    def get_ordered(cls, criteria, direction, *args):
        return cls.get_by_filter("1 = 1 ORDER BY %s %s" % (criteria, direction), *args)

    def create(self, cls, tablename, fieldnames, *args, **kwargs):
        empty_fields = set(fieldnames)
        field_values = {}

        for key, value in args[0].iteritems():
            if key not in fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        field_values.pop('id')
        fieldnames.remove('id')

        query = "INSERT INTO %s (%s) VALUES (%s) RETURNING id" % (
                                       tablename,
                                       ', '.join(field_values.keys()),
                                       ', '.join(['%s'] * len(fieldnames)))

        fieldnames.insert(0, 'id')

        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute(query, field_values.values())
        _id = cursor.fetchone()
        con.commit()
        return cls.get(id=_id[0])

    def delete(self):
        query = "DELETE FROM %s WHERE id=%%s" % (self.tablename)
        cur.execute(query, [self.id])


class MySQLAdaptor(Adaptor):

    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    def get_connection(self):
        import MySQLdb
        con = MySQLdb.connect(host=self.host,
                              db=self.database,
                              user=self.username,
                              passwd=self.password)
        return con

    def get_by_sql(self, query, *args):
        cur = self.get_connection().cursor()
        cur.execute(query)
        return cur.fetchall()

    def get_by_filter(self, filter, *args):
        tablename = args[0]
        fieldnames = args[1]
        query = "SELECT %s FROM %s WHERE %s" % (', '.join(fieldnames),
                                                tablename,
                                                filter)
        return self.get_by_sql(query, *args)

    def get_all(cls, *args):
        return cls.get_by_filter("1 = 1", *args)

    def get_ordered(cls, criteria, direction, *args):
        return cls.get_by_filter("1 = 1 ORDER BY %s %s" % (criteria, direction), *args)

    def get_last_inserted_id(self, con):
        cur = con.cursor()
        cur.execute("""SELECT last_insert_id()""")
        return cur.fetchone()[0]

    def create(self, cls, tablename, fieldnames, *args, **kwargs):
        empty_fields = set(fieldnames)
        field_values = {}

        for key, value in args[0].iteritems():
            if key not in fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                            tablename,
                                            ', '.join(field_values.keys()),
                                            ', '.join(['%s'] * len(fieldnames)))

        con = self.get_connection()
        con.cursor().execute(query, field_values.values())
        con.commit()
        return cls.get(id=self.get_last_inserted_id(con))

    def delete(self):
        query = "DELETE FROM %s WHERE id=%%s" % (self.tablename)
        cur.execute(query, [self.id])



class SQLiteAdaptor(Adaptor):

    def __init__(self, database):
        self.database = database

    def get_connection(self):
        import sqlite3
        con = sqlite3.connect(self.database)
        return con

    def get_by_sql(self, query, *args):
        cur = self.get_connection().cursor()
        cur.execute(query)
        return cur.fetchall()

    def get_by_filter(self, filter, *args):
        tablename = args[0]
        fieldnames = args[1]
        query = "SELECT %s FROM %s WHERE %s" % (', '.join(fieldnames),
                                                tablename,
                                                filter)
        return self.get_by_sql(query, *args)

    def get_all(cls, *args):
        return cls.get_by_filter("1 = 1", *args)

    def get_ordered(cls, criteria, direction, *args):
        return cls.get_by_filter("1 = 1 ORDER BY %s %s" % (criteria, direction), *args)

    def get_last_inserted_id(self, con):
        cur = con.cursor()
        cur.execute("""SELECT last_insert_rowid()""")
        return cur.fetchone()[0]

    def create(self, cls, tablename, fieldnames, *args, **kwargs):
        empty_fields = set(fieldnames)
        field_values = {}

        for key, value in args[0].iteritems():
            if key not in fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                       tablename,
                                       ', '.join(field_values.keys()),
                                       ', '.join(['?'] * len(fieldnames)))

        values = []
        for value in field_values.values():
            values.append(value)

        con = self.get_connection()
        con.cursor().execute(query, values)
        con.commit()
        return cls.get(id=self.get_last_inserted_id(con))

    def update(self, tablename, fieldnames, *args):
        _object = args[0]

        settings = ""
        for fieldname in fieldnames:
            settings += ", " + fieldname + "=?"
        settings = settings[2:]

        values = []
        for fieldname in fieldnames:
            values.append(str(getattr(_object, fieldname)))

        query = "UPDATE %s SET %s WHERE id = %s" % (tablename, settings, _object.id)

        con = self.get_connection()
        con.cursor().execute(query, values)
        con.commit()






class MyDbAdaptor(Adaptor):

    import db_driver
    def __init__(self, database):
        self.database = database

    def get_connection(self):
        con = db_driver.connect(self.database)
        return con

    def get_by_sql(self, query, *args):
        con = self.get_connection()
        return con.execute(query)

    def get_by_filter(self, filter, *args):
        tablename = args[0]
        fieldnames = args[1]
        query = "SELECT %s FROM %s WHERE %s" % (', '.join(fieldnames),
                                                tablename,
                                                filter)
        return self.get_by_sql(query, *args)

    def get_ordered(cls, criteria, direction, *args):
        return cls.get_by_filter("1=1 ORDER BY %s %s" % (criteria, direction), *args)

    def get_all(cls, *args):
        return cls.get_by_filter("1=1", *args)

    def update(self, tablename, fieldnames, *args):
        _object = args[0]
        settings = ""
        for fieldname in fieldnames:
            settings += ", " + fieldname + "=%s"
        settings = settings[2:]

        query = "UPDATE %s SET %s WHERE id=%%s" % (tablename, settings)

        values = []
        for fieldname in fieldnames:
            values.append(getattr(_object, fieldname))
        values.append(_object.id)

        con = self.get_connection()
        con.execute(query % tuple(values))

    def create(self, cls, tablename, fieldnames, *args, **kwargs):
        empty_fields = set(fieldnames)
        field_values = {}

        for key, value in args[0].iteritems():
            if key not in fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                       tablename,
                                       ', '.join(field_values.keys()),
                                       ', '.join(['%s'] * len(fieldnames)))

        values = []
        for value in field_values.values():
            values.append(value)

        con = self.get_connection()
        return cls.get(id=con.execute(query % tuple(values)))
