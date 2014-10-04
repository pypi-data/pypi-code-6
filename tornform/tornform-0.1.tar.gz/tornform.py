# -*- coding: utf-8 -*-
from decimal import Decimal
from voluptuous import MultipleInvalid
from datetime import datetime, date


__version__ = '0.1'


class EmptyDict(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        return self[name] if name in self else ''


class InvalidSchemaError(Exception):
    pass


class Form(object):
    def __init__(self, schema, arguments=None, dt_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d', decimal_fmt=str):
        """
        @type arguments dict
        @type schema Schema
        """
        self._arguments = dict()
        self._schema = schema
        self._filtered = None
        self.error = EmptyDict()

        if arguments is None:
            arguments = {}

        def mixstr(v):
            vt = type(v)  # 为了效率 简单粗暴
            if vt != str:
                if v is None:
                    v = ''
                elif vt == unicode:
                    v = v.encode('utf-8')
                elif vt == datetime:
                    v = v.strftime(dt_fmt)
                elif vt == date:
                    v = v.strftime(date_fmt)
                elif vt == Decimal:
                    v = decimal_fmt(v)
                else:
                    v = str(v)
            return v

        for name in self._schema.schema:
            key = str(name)
            if key in ('error', 'valid', 'filtered', '_filtered', '_schema', '_arguments'):
                raise InvalidSchemaError('key %s not allowed.', key)

            require_list = key.endswith('[]')

            if key not in arguments:
                self._arguments[key] = [] if require_list else ''
                continue

            value = arguments[key]
            if isinstance(value, list):
                value = [mixstr(item) for item in value]
            else:
                value = [mixstr(value)]

            if not require_list:
                value = value[0]
            self._arguments[key] = value

    def __getattr__(self, item):
        if item not in self._arguments:
            item += '[]'
        return self._arguments.get(item, '')

    @property
    def valid(self):
        if self._filtered is not None:
            return True

        try:
            self._filtered = EmptyDict({k.rstrip('[]'): v for (k, v) in self._schema(self._arguments).items()})
            return True
        except MultipleInvalid as e:
            for error in e.errors:
                name = str(error.path[0] if type(error.path) == list else error.path)
                if name not in self.error:
                    self.error[name] = str(error)
            return False

    @property
    def filtered(self):
        return self._filtered if self.valid else EmptyDict()
