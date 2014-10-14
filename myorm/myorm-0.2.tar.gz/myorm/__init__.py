#!/usr/bin/env python
# coding: utf-8

AUTHOR = "Christian Kokoska"

from flask import g

class InvalidFieldName(Exception):
    pass


class Dbobject(object):
    """
    The main model which provides the ORM
    """

    @classmethod
    def get_by_sql(cls, query, *args):
        g.cur.execute(query, *args)
        return [cls(*item) for item in g.cur.fetchall()]

    @classmethod
    def get_by_filter(cls, filter, *args):
        query = "SELECT %s FROM %s WHERE %s" % (', '.join(cls.fieldnames),
                                                cls.tablename,
                                                filter)
        return cls.get_by_sql(query, *args)

    @classmethod
    def get_all(cls):
        return cls.get_by_filter("1 = 1")

    @classmethod
    def get_ordered(cls, criteria, direction):
        return cls.get_by_filter("1 = 1 ORDER BY %s %s" % (criteria, direction))

    def save(self):
        if self.id:
            self.update()
        else:
            self.insert()

    def insert(self):
        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                       self.tablename,
                                       ', '.join(self.fieldnames),
                                       ', '.join(['%s'] * len(self.fieldnames)))

        values = []
        for name in self.fieldnames:
            values.append(getattr(self, name))

        g.cur.execute(query, values)

    def update(self):
        settings = ""
        for fieldname in self.fieldnames:
            settings += " ," + fieldname + "=%s"
        settings = settings[2:]

        query = "UPDATE %s SET %s WHERE id = %%s" % (self.tablename, settings)

        values = []
        for fieldname in self.fieldnames:
            values.append(getattr(self, fieldname))
        values.append(self.id)

        g.cur.execute(query, values)

    def delete(self):
        query = "DELETE FROM %s WHERE id=%%s" % (self.tablename)
        g.cur.execute(query, [self.id])


class MySQLObject(Dbobject):
    
    @staticmethod
    def get_last_inserted_id():
        g.cur.execute("""SELECT last_insert_id()""")
        return g.cur.fetchone()[0]

    @classmethod
    def get_by_id(cls, id):
        return cls.get_by_filter("id = %s", id)[0]

    @classmethod
    def create(cls, *args, **kwargs):

        empty_fields = set(cls.fieldnames)
        field_values = {}

        for key, value in kwargs.iteritems():
            if key not in cls.fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                       cls.tablename,
                                       ', '.join(field_values.keys()),
                                       ', '.join(['%s'] * len(cls.fieldnames)))

        g.cur.execute(query, field_values.values())
        g.con.commit()
        return cls.get_by_id(cls.get_last_inserted_id())


class SQLiteObject(Dbobject):

    @staticmethod
    def get_last_inserted_id():
        g.cur.execute("""SELECT last_insert_rowid()""")
        return g.cur.fetchone()[0]

    @classmethod
    def get_by_id(cls, id):
        return cls.get_by_filter("id = %s" % id)[0]


    @classmethod
    def create(cls, *args, **kwargs):

        empty_fields = set(cls.fieldnames)
        field_values = {}

        for key, value in kwargs.iteritems():
            if key not in cls.fieldnames:
                raise InvalidFieldName
            else:
                empty_fields -= set([key])
                field_values[key] = value

        for key in empty_fields:
            field_values[key] = None

        query = "INSERT INTO %s (%s) VALUES (%s)" % (
                                       cls.tablename,
                                       ', '.join(field_values.keys()),
                                       ', '.join(['?'] * len(cls.fieldnames)))

        g.cur.execute(query, field_values.values())
        g.con.commit()
        return cls.get_by_id(cls.get_last_inserted_id())
