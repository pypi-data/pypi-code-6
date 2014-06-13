import inspect


class DependencyNotFound(AttributeError):
    pass


class WaiterTimeout(Exception):
    pass


class ContainerBeingKilled(Exception):
    """Raised by :meth:`Container.spawn_worker` if it has started a ``kill``
    sequence.

    Entrypoint providers should catch this and react as if they hadn't been
    available in the first place, e.g. an rpc consumer should probably requeue
    the message.

    We need this because eventlet may yield during the execution of
    :meth:`Container.kill`, giving entrypoints a chance to fire before
    they themselves have been killed.
    """


registry = {}


def get_module_path(exc_type):
    """ Return the dotted module path of `exc_type`, including the class name.

    e.g.::

        >>> get_module_path(MethodNotFound)
        >>> "nameko.exceptions.MethodNotFound"

    """
    module = inspect.getmodule(exc_type)
    return "{}.{}".format(module.__name__, exc_type.__name__)


class RemoteError(Exception):
    """ Exception to raise at the caller if an exception occured in the
    remote worker.
    """
    def __init__(self, exc_type=None, value=""):
        self.exc_type = exc_type
        self.value = value
        message = '{} {}'.format(exc_type, value)
        super(RemoteError, self).__init__(message)


def serialize(exc):
    """ Serialize `self.exc` into a data dictionary representing it.
    """
    return {
        'exc_type': type(exc).__name__,
        'exc_path': get_module_path(type(exc)),
        'exc_args': exc.args,
        'value': unicode(exc),
    }


def deserialize(data):
    """ Deserialize `data` to an exception instance.

    If the `exc_path` value matches an exception registered as
    ``deserializable``, return an instance of that exception type.
    Otherwise, return a `RemoteError` instance describing the exception
    that occured.
    """
    key = data.get('exc_path')
    if key in registry:
        exc_args = data.get('exc_args', ())
        return registry[key](*exc_args)

    exc_type = data.get('exc_type')
    value = data.get('value')
    return RemoteError(exc_type=exc_type, value=value)


def deserialize_to_instance(exc_type):
    """ Decorator that registers `exc_type` as deserializable back into an
    instance, rather than a :class:`RemoteError`. See :func:`deserialize`.
    """
    key = get_module_path(exc_type)
    registry[key] = exc_type
    return exc_type


@deserialize_to_instance
class MethodNotFound(Exception):
    pass


@deserialize_to_instance
class IncorrectSignature(Exception):
    pass


class UnknownService(Exception):
    def __init__(self, service_name):
        self._service_name = service_name
        super(UnknownService, self).__init__(service_name)

    def __str__(self):
        return "Unknown service `{}`".format(self._service_name)


class UnserializableValueError(Exception):
    def __init__(self, value):
        self.repr_value = repr(value)
        super(UnserializableValueError, self).__init__()

    def __str__(self):
        return "Unserializable value: `{}`".format(self.repr_value)
