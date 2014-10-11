# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import time
import datetime

from django.db import models
from django.utils import datetime_safe
from six import string_types

from ox.utils import json


def to_json(python_object):
    if isinstance(python_object, datetime.datetime):
        if python_object.year < 1900:
            tt = python_object.timetuple()
            value = '%d-%02d-%02dT%02d:%02d%02dZ' % tuple(list(tt)[:6])
        else:
            value = python_object.strftime('%Y-%m-%dT%H:%M:%SZ')
        return {'__class__': 'datetime.datetime',
                '__value__': value}
    if isinstance(python_object, datetime_safe.datetime):
        return {'__class__': 'datetime.datetime',
                '__value__': python_object.strftime('%Y-%m-%dT%H:%M:%SZ')}
    if isinstance(python_object, time.struct_time):
        return {'__class__': 'time.asctime',
                '__value__': time.asctime(python_object)}
    try:
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                '__value__': list(python_object)}
    except:
        pass
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])
        if json_object['__class__'] == 'datetime_safe.datetime' \
            or json_object['__class__'] == 'datetime.datetime':
            return datetime_safe.datetime.strptime(json_object['__value__'], '%Y-%m-%dT%H:%M:%SZ')
        if json_object['__class__'] == 'time.asctime':
            return time.strptime(json_object['__value__'])
    return json_object

class DictField(models.TextField):
    """DictField is a textfield that contains JSON-serialized dictionaries."""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to python after we load it from the DB"""
        if value == None:
            return value
        if isinstance(value, dict):
            return value
        try:
            value = json.loads(value, object_hook=from_json)
        except: #this is required to load fixtures
            value = eval(value)
        assert isinstance(value, dict)
        return value

    def get_db_prep_save(self, value, connection):
        """Convert our JSON object to a string before we save"""
        if value == None:
            return value
        if isinstance(value, string_types):
            value = eval(value)
        assert isinstance(value, dict)
        value = json.dumps(value, default=to_json)
        return super(DictField, self).get_db_prep_save(value, connection=connection)

class TupleField(models.TextField):
    """TupleField is a textfield that contains JSON-serialized tuples."""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if isinstance(value, tuple):
            return value

        try:
            value = json.loads(value, object_hook=from_json)
        except: #this is required to load fixtures
            value = eval(value)
        assert isinstance(value, list)
        return tuple(value)

    def get_db_prep_save(self, value, connection):
        """Convert our JSON object to a string before we save"""
        if isinstance(value, string_types):
            value = eval(value)
            if isinstance(value, list):
                value = tuple(value)
        assert isinstance(value, tuple)
        value = json.dumps(value, default=to_json)
        return super(TupleField, self).get_db_prep_save(value, connection=connection)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^ox.django\.fields\.DictField"])
    add_introspection_rules([], ["^ox.django\.fields\.TupleField"])
except:
    pass
