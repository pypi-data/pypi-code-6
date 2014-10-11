# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from django.db.models.sql import Query
from django.db.models.sql.compiler import SQLCompiler
from django.db import connections
import django.db.models.query

'''
models.py:
-----------------------------------
from ox.django.query import QuerySet

class Manager(models.Manager):
    def get_query_set(self):
        return QuerySet(self.model)

class Model(models.Model):
    ...
    objects = Manager()
'''

class SQLCompiler(SQLCompiler):

    def get_ordering(self):
        result, group_by = super(SQLCompiler, self).get_ordering()
        if self.query.nulls_last and len(result):
            if self.connection.vendor == 'sqlite':
                _result = []
                for r in result:
                    if r.endswith(' DESC'):
                        _r = r[:-len(' DESC')]
                    elif r.endswith(' ASC'):
                        _r = r[:-len(' ASC')]
                    _result.append(_r + ' IS NULL')
                    _result.append(r)

                result = _result
            else:
                result = map(lambda e: e + ' NULLS LAST', result)
        return result, group_by

class Query(Query):
    nulls_last = False

    def clone(self, *args, **kwargs):
        obj = super(Query, self).clone(*args, **kwargs)
        obj.nulls_last = self.nulls_last
        return obj

    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]
        # Check that the compiler will be able to execute the query
        for alias, aggregate in self.aggregate_select.items():
            connection.ops.check_aggregate_support(aggregate)
        
        return SQLCompiler(self, connection, using)


class QuerySet(django.db.models.query.QuerySet):

    def __init__(self, model=None, query=None, using=None, **kwargs):
        super(QuerySet, self).__init__(model=model, query=query, using=None, **kwargs)
        self.query = query or Query(self.model)

    def order_by(self, *args, **kwargs):
        nulls_last = kwargs.pop('nulls_last', False)
        obj = super(QuerySet, self).order_by(*args, **kwargs)
        obj.query.nulls_last = nulls_last
        return obj
