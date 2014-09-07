import json
from select import select


class MessageError(Exception):

    pass


class MessageNamespaceSet(object):

    def __init__(self):
        self.namespaces = {}
        x = self.register("messaging")
        x.register("error", Message.DIRECTION_CLIENT)

    def register(self, code, silent=False):
        try:
            x = self.namespaces[code]
            if silent:
                return x
            else:
                raise MessageError("Message namespace already registered", code="messaging:namespace:already-exists")
        except KeyError:
            x = MessageNamespace(code)
            self.namespaces[code] = x
            return x

    def find(self, code):
        try:
            return self.namespaces[code]
        except KeyError:
            raise MessageError("Message namespace not registered", code="messaging:namespace:does-not-exist")

    def unserialize(self, obj, must_be_serverwise=False):
        if not isinstance(obj['code'], basestring) or not isinstance(obj['args'], list) or not isinstance(obj['kwargs'], dict):
            e = MessageError("Expected format message is {code:string, args:list, kwargs:dict}", code="messaging:message:invalid")
            e.message_parts = obj
            raise e
        else:
            code_parts = obj['code'].split(".")
            if len(code_parts) != 2:
                e = MessageError("Message code must be in format `namespace.code`. Current: " + obj.code, code="messaging:message:invalid")
                e.message_parts = obj
                raise e
            else:
                try:
                    factory = self.find(code_parts[0]).find(code_parts[1])
                    if must_be_serverwise and not (factory.direction & Message.DIRECTION_SERVER):
                        raise MessageError("Message cannot be unserialized since it's not server-wise", code="messaging:message:not-server-wise")
                    return factory.build_message(*obj['args'], **obj['kwargs'])
                except MessageError as e:
                    e.message_parts = obj
                    raise e

    def unserialize_json(self, val, must_be_serverwise=False):
        try:
            return self.unserialize(json.loads(val), must_be_serverwise)
        except ValueError as e:
            e.value = val
            raise e


class MessageNamespace(object):

    def __init__(self, ns):
        self.ns = ns
        self.messages = {}

    def register(self, code, direction, silent=False):
        try:
            x = self.messages[code]
            if silent:
                return x
            else:
                raise MessageError("Message already registered", code="messaging:factory:already-exists")
        except KeyError:
            x = MessageFactory(self.ns, code, direction)
            self.messages[code] = x
            return x

    def find(self, code):
        try:
            return self.messages[code]
        except KeyError:
            raise MessageError("Message not registered", code="messaging:factory:does-not-exist")


class MessageFactory(object):

    def __init__(self, ns, code, direction):
        self.ns = ns
        self.code = code
        self.direction = direction

    def build_message(self, *args, **kwargs):
        return Message(self.ns, self.code, self.direction, *args, **kwargs)


class Message(object):

    DIRECTION_CLIENT = 1
    DIRECTION_SERVER = 2
    DIRECTION_BOTH = DIRECTION_CLIENT | DIRECTION_SERVER

    def __init__(self, ns, code, direction, *args, **kwargs):
        self.ns = ns
        self.code = code
        self.args = args
        self.kwargs = kwargs
        self.direction = direction

    def is_code(self, ns, code):
        return self.ns == ns and self.code == code

    def serialize(self, must_be_clientwise=False):
        if must_be_clientwise and not (self.direction & Message.DIRECTION_CLIENT):
            raise MessageError("Message cannot be serialized since it's not client-wise", code="messaging:message:not-client-wise")

        return {
            "code": "%s.%s" % (self.ns, self.code),
            "args": self.args,
            "kwargs": self.kwargs
        }

    def serialize_json(self, must_be_clientwise=False):
        return json.dumps(self.serialize(must_be_clientwise))