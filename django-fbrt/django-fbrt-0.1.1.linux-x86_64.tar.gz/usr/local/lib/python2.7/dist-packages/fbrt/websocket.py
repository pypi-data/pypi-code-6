from select import select
from messaging import *
from django.conf import settings


class LoopError(Exception):
    pass


class InvalidFormatError(LoopError):
    pass


class ProtocolViolationError(LoopError):
    pass


class Loop(object):

    def __init__(self, request, websocket, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.websocket = websocket

    def welcome(self):
        pass

    def goodbye(self):
        pass

    def process(self):
        pass

    def raise_invalid_format(self, message):
        x = InvalidFormatError()
        x.data = message
        raise x

    def raise_protocol_violation(self, message):
        x = ProtocolViolationError()
        x.data = message
        raise x

    def __call__(self):
        ws_sock = self.websocket.handler.socket.fileno()
        self.welcome()
        while not self.websocket.closed:
            select([ws_sock], [], [])
            if self.process() is False:
                break
        self.goodbye()

    @classmethod
    def as_view(cls):
        def wrapped(request, websocket, *args, **kwargs):
            instance = cls(request, websocket, *args, **kwargs)
            try:
                instance()
                if not websocket.closed:
                    websocket.close(1000)
            #TO-DO: 1002 para error de protocolo (e.g. no debe mandar ese mensaje)
            #TO-DO: 1003 para formato de mensaje no aceptado
            except ProtocolViolationError as e:
                if settings.DEBUG:
                    websocket.close(1002, "Unexistent or unavailable message: " + repr(e.data))
                else:
                    websocket.close(1002, "Unexistent or unavailable message")
            except InvalidFormatError as e:
                if settings.DEBUG:
                    websocket.close(1003, "Message format error for: " + repr(e.data))
                else:
                    websocket.close(1003, "Message format error")
            except Exception as e:
                if settings.DEBUG:
                    websocket.close(1011, "Cannot fullfill request: Exception triggered: %s - %s" % (type(e).__name__, str(e)))
                else:
                    websocket.close(1011, "Cannot fullfill request: Internal server error")
        return wrapped


class MessageLoop(Loop):

    def __init__(self, strict=False, *args, **kwargs):
        super(MessageLoop, self).__init__(*args, **kwargs)
        self._ns_set = MessageNamespaceSet()
        self.strict = strict
        setup = self.namespaces_setup()
        opts = {
            "server": Message.DIRECTION_SERVER,
            "client": Message.DIRECTION_CLIENT,
            "both": Message.DIRECTION_BOTH
        }
        for k, v in setup.iteritems():
            x = self._ns_set.register(k, True)
            for k2, d in v.iteritems():
                x.register(k2, opts[d.lower()], True)

    def namespaces_setup(self):
        """
        Inicializa los comandos disponibles que queramos darle.
        """
        return {}

    def process(self):
        received = self.websocket.receive()
        try:
            return self.message(self.namespace_set.unserialize_json(received, True))
        except (ValueError, MessageError) as error:
            if self.strict:
                if (isinstance(error, MessageError) and getattr(error, 'code', False) == "messaging:message:invalid") or isinstance(error, ValueError):
                    return self.raise_invalid_format(error.message_parts)
                else:
                    return self.raise_protocol_violation(error.message_parts)
            return self.invalid(error)
        except Exception as error:
            if self.strict:
                raise error
            return self.invalid(error)

    def send_message(self, ns, code, *args, **kwargs):
        self.websocket.send(self.namespace_set.find(ns).find(code).build_message(*args, **kwargs).serialize_json(True))

    def message(self, message):
        pass

    def invalid(self, error):
        pass

    @property
    def namespace_set(self):
        return self._ns_set