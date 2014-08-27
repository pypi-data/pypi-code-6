
from __future__ import unicode_literals, print_function, absolute_import

import json
import time
import datetime
import flask
import traceback
import logging

_logger = logging.getLogger(__name__)

def _datetime_to_timestamp(dat):
    ts = time.mktime(dat.timetuple())
    return ts + (dat.microsecond / 1000000.)

def _fqn(c):
  return c.__module__ + "." + c.__name__

class TypeHandler(object):

    python_type = None
    type_identifier = None

    def from_json(self, dictionary, continue_func):
        pass

    def to_json(self, obj, continue_func):
        pass

class DateTimeHandler(TypeHandler):
    """
    Handles datetime.datetime objects for serialization. datetime.datetime are always assumed to be
    naive and in the local timezone. The json-compatible format uses a Unix timestamp, counting the
    number of milli-seconds since the epoch in the UTC timezone.
    """

    python_type = datetime.datetime
    type_identifier = "datetime"

    def from_json(self, dictionary, continue_func):
        return datetime.datetime.fromtimestamp(dictionary["timestamp"] / 1000.)

    def to_json(self, obj, continue_func):
        return {"timestamp": int(_datetime_to_timestamp(obj) * 1000.)}

class DateHandler(TypeHandler):
    """
    Handles datetime.date objects for serialization. The json-compatible format uses a dictionary
    containing the keys "year", "month" (1-12) and "day"(1-31). 
    """

    python_type = datetime.date
    type_identifier = "date"

    def from_json(self, dictionary, continue_func):
        return datetime.date(dictionary["year"], dictionary["month"], dictionary["day"])

    def to_json(self, obj, continue_func):
        return {"year": obj.year, "month": obj.month, "day": obj.day}

class GenericJsonException(Exception):
    def __init__(self, message, type_, traceback=None):
        self.message = message
        self.type = type_
        self.traceback = traceback
        super(GenericJsonException, self).__init__(message, type_, traceback)

def to_json_exception(obj):
    return GenericJsonException(obj.message, _fqn(type(obj)))

class ExceptionHandler(TypeHandler):
    """
    Handles datetime.datetime objects for serialization. datetime.datetime are always assumed to be
    naive and in the local timezone. The json-compatible format uses a Unix timestamp, counting the
    number of milli-seconds since the epoch in the UTC timezone.
    """

    python_type = Exception
    type_identifier = "exception"

    def from_json(self, dictionary, continue_func):
        return GenericJsonException(dictionary["message"], dictionary["type"], dictionary["traceback"])

    def to_json(self, obj, continue_func):
        if not isinstance(obj, GenericJsonException):
            obj = to_json_exception(obj)
        return {"type": obj.type, "message": obj.message, "traceback": obj.traceback}

class JsonSerializer(object):

    def __init__(self):
        self.handlers = {}
        self.handlers_list = []
        self.add_handler(ExceptionHandler())
        self.add_handler(DateTimeHandler())
        self.add_handler(DateHandler())
    
    def to_json_types(self, data):
        if isinstance(data, (int, long, str, unicode, float, bool, type(None))):
            return data
        elif isinstance(data, (list, tuple)):
            nl = []
            for i in data:
                nl.append(self.to_json_types(i))
            return nl
        elif isinstance(data, dict):
            nd = {}
            for k, v in data.items():
                nd[k] = self.to_json_types(v)
            return nd
        for handler in self.handlers_list:
            if isinstance(data, handler.__class__.python_type):
                dct = handler.to_json(data, self.to_json_types)
                dct["__type__"] = handler.__class__.type_identifier
                return dct
        raise JsonSerializerException("Impossible to serialize type %s" % type(data))

    def from_json_types(self, data):
        if isinstance(data, (int, long, str, unicode, float, bool, type(None))):
            return data
        elif isinstance(data, (list, tuple)):
            nl = []
            for i in data:
                nl.append(self.from_json_types(i))
            return nl
        elif isinstance(data, dict):
            if "__type__" in data:
                handler = self.handlers.get(data["__type__"])
                if not handler:
                    raise JsonSerializerException("Could not find handler for type '%s'" % data["__type__"])
                return handler.from_json(data, self.from_json_types)
            else:
                nd = {}
                for k, v in data.items():
                    nd[k] = self.from_json_types(v)
                return nd
        raise JsonSerializerException("Unknown type: %s" % type(data))

    def stringify(self, data):
        conv = self.to_json_types(data)
        return json.dumps(conv, sort_keys=True)

    def parse(self, text):
        to_conv = json.loads(text)
        return self.from_json_types(to_conv)

    def add_handler(self, handler):
        assert isinstance(handler, TypeHandler), "Expected object implementing TypeHandler: %s" % handler
        self.handlers[handler.__class__.type_identifier] = handler
        self.handlers_list.append(handler)

class JsonSerializerException(Exception):
    pass

class JsonCommunicator(object):
    def __init__(self):
        self.json_serializer = JsonSerializer()
        self.debug = True

    def receive(self, flask_request, callback):
        content = flask_request.get_json()
        arguments = self.json_serializer.from_json_types(content)
        assert isinstance(arguments, list), "Expected list: %s" % arguments
        error = False
        try:
            ret = callback(*arguments)
        except Exception as e:
            _logger.exception("Exception during request")
            nex = to_json_exception(e)
            if self.debug:
                nex.traceback = traceback.format_exc()
            error = True
            ret = nex
        resp = flask.make_response(self.json_serializer.stringify(ret), 500 if error else 200)
        resp.mimetype = "application/json"
        return resp
