from __future__ import unicode_literals

from django.core import serializers
from django.core.serializers.python import Deserializer
from django.db.models import Model
import datetime
import decimal
import json
from uuid import uuid4
from django.utils.timezone import is_aware


# Workaround for python3
try:
    iteritems = dict.iteritems
except AttributeError:
    iteritems = dict.items


def serialize(obj):
    return json.dumps(obj, cls=DjangoJSONEncoder)


def deserialize(string):
    return json.loads(string, cls=DjangoJSONDecoder)


class DjangoJSONEncoder(json.JSONEncoder):
    """
    Inspired by the json serializer of Django with slightly changes.

    Source: https://github.com/django/django/blob/1.7c2/django/core/serializers/json.py
    """
    def __init__(self, *args, **kwargs):
        super(DjangoJSONEncoder, self).__init__(*args, **kwargs)
        self._replacement_map = {}

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif issubclass(o.__class__, Model):
            # Serialize object and remove surrounding parenthesis
            obj = serializers.serialize('json', [o, ])[1:-1]
            key = uuid4().hex
            self._replacement_map[key] = obj
            # print self._replacement_map
            return key
        else:
            return super(DjangoJSONEncoder, self).default(o)

    def encode(self, o):
        result = super(DjangoJSONEncoder, self).encode(o)

        for k, v in iteritems(self._replacement_map):
            result = result.replace('"%s"' % (k,), v)

        return result


class DjangoJSONDecoder(json.JSONDecoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def decode(self, s):
        o = super(DjangoJSONDecoder, self).decode(s)
        return self.check_for_models(o)

    def check_for_models(self, i):

        if not isinstance(i, (dict, list)):
            return i

        if isinstance(i, list):
            n = len(i)
            while n:
                n -= 1
                i[n] = self.check_for_models(i[n])

            return i

        k = i.keys()
        if 'model' in k and 'fields' in k:
            # It's a model
            for g in Deserializer([i]):
                # g is a DeserializedObject instance
                # See: https://github.com/django/django/blob/master/django/core/serializers/base.py
                #
                # Just return it and ignore the stuff around
                return g.object

        for n, val in iteritems(i):
            i[n] = self.check_for_models(i[n])

        return i