from infi.traceback import traceback_decorator
from infi.pyutils.contexts import contextmanager
import gevent

from logbook import Logger
logger = Logger(__name__)

_uncaught_exception_handler = None


def set_greenlet_uncaught_exception_handler(func):
    """
    Sets a global greenlet uncaught exception handler that will get called if a greenlet spawned by one of this module's
    wrappers raises an uncaught exception.
    :param func: exception handler function that will receive the exc_info tuple as an argument
    :returns: previous exception handler function or None
    """
    global _uncaught_exception_handler
    prev_handler, _uncaught_exception_handler = _uncaught_exception_handler, func
    return prev_handler


@traceback_decorator
def uncaught_greenlet_exception():
    global _uncaught_exception_handler
    if _uncaught_exception_handler:
        _uncaught_exception_handler()
    else:
        logger.exception("uncaught exception in greenlet and uncaught exception handler was set")


@contextmanager
def uncaught_greenlet_exception_context():
    try:
        yield
    except gevent.GreenletExit:
        raise
    except:
        uncaught_greenlet_exception()


def _normalize_instancemethod(instance_method):
    """
    wraps(instancemethod) returns a function, not an instancemethod so its repr() is all messed up;
    we want the original repr to show up in the logs, therefore we do this trick
    """
    if not hasattr(instance_method, 'im_self'):
        return instance_method

    def _func(*args, **kwargs):
        return instance_method(*args, **kwargs)

    _func.__name__ = repr(instance_method)
    return _func


def wrap_uncaught_greenlet_exceptions(func):
    def _func(*args, **kwargs):
        with uncaught_greenlet_exception_context():
            return func(*args, **kwargs)
    _func.__name__ = repr(func)
    return _func


def safe_spawn(func, *args, **kwargs):
    return gevent.spawn(wrap_uncaught_greenlet_exceptions(func), *args, **kwargs)


def safe_spawn_later(seconds, func, *args, **kwargs):
    return gevent.spawn_later(seconds, wrap_uncaught_greenlet_exceptions(func), *args, **kwargs)


def safe_spawn_and_switch_immediately(func, *args, **kwargs):
    greenlet = safe_spawn(func, *args, **kwargs)
    gevent.sleep(0)
    return greenlet








































# def die_on_uncaught_exception_handler(exc_info):
#     pass


# def die_on_greenlet_exceptions(func):
#     @wraps(func)
#     def decorated_func(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except gevent.GreenletExit:
#             raise
#         except:

#             reason = "{} raised exception in greenlet and not caught, exitting process.".format(func)
#             die_now_and_dont_look_back(reason=reason, exc_info=exc_info())
#     return traceback_decorator(decorated_func)


# def return_exceptions_in_greenlet(func):
#     @wraps(func)
#     def decorated_func(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except gevent.GreenletExit:
#             raise
#         except:
#             logger.exception("{} raised exception in greenlet and not caught, returning the exception", func)
#             return exc_info()[1]
#     return traceback_decorator(decorated_func)






# def joinall(greenlets, timeout=None, raise_error=False):
#     """wrapper for gevent.joinall
#     if the greenlet that waits for the joins is killed, it kills all the greenlets it joins for"""
#     greenlets = list(greenlets)
#     try:
#         gevent.joinall(greenlets, timeout=timeout, raise_error=raise_error)
#     except gevent.GreenletExit:
#         [greenlet.kill() for greenlet in greenlets if not greenlet.ready()]
#         raise
#     return greenlets


# def get_running_greenlets():
#     from gc import get_objects
#     return [item for item in get_objects() if isinstance(item, gevent.Greenlet) and item.started and not item.ready()]


# def default_die_now_callback(exitcode=10, reason=None, exc_info=None):
#     from infi.tracing import wait_and_ensure_exit
#     from izbox.utils import sleep
#     wait_and_ensure_exit(5, exitcode)  # wait 5 seconds before terminating the process

#     try:
#         from izbox.logging import logbook_application_setup
#         from izbox.logging.tracing import unset_tracing
#         if reason:
#             logger.error(reason, exc_info=exc_info)
#         sleep(3)  # needed for log messages to be flushed out
#         try:
#             logbook_application_setup.__exit__(None, None, None)  # give the logging handlers a chance to dump
#         except AssertionError:  # this happens, not sure why
#             pass

#         unset_tracing()
#     finally:
#         sleep(1000000)  # never reach here.


# def get_die_now_callback_that_generates_an_event(configuration):
#     from izbox.events import EventFactory
#     from izbox.utils import get_process_name
#     from os import getpid
#     factory = EventFactory(configuration)

#     def generate_event_die_now_callback(exitcode=10, reason=None, exc_info=None):
#         try:
#             factory.process_suicide(name=get_process_name(), pid=getpid(), exitcode=exitcode, reason=reason,
#                                     exc_info=exc_info)
#         finally:
#             default_die_now_callback(exitcode=exitcode, reason=reason, exc_info=exc_info)

#     return generate_event_die_now_callback


# die_now_callback = default_die_now_callback


# def register_die_now_callback(callback):
#     global die_now_callback
#     previous_handler = die_now_callback
#     die_now_callback = callback
#     return previous_handler


# def die_now_and_dont_look_back(exitcode=10, reason=None, exc_info=None):
#     global die_now_callback
#     die_now_callback(exitcode, reason, exc_info)


# def get_die_now_and_dont_look_back_on_signal(signal_string):
#     def func():
#         die_now_and_dont_look_back(reason=signal_string)
#     return func


# def handle_error(context, type, value, tb):
#     # the original function just logs the exceptions to stderr
#     if issubclass(type, KeyboardInterrupt):
#         original_hub_system_error(type, value)
#         return
#     die_now_and_dont_look_back(reason="gevent hub error: {}".format(value), exc_info=(type, value, tb))


# def handle_system_error(type, value):
#     # the original function just logs the exceptions to stderr
#     die_now_and_dont_look_back(reason="gevent hub system error: {!r}".format(value), exc_info=exc_info())


# sleep = gevent.sleep
# getcurrent = gevent.getcurrent
# Event = gevent.event.Event
# AsyncResult = gevent.event.AsyncResult
# queue = gevent.queue
# original_hub_system_error = gevent.get_hub().handle_system_error
# gevent.get_hub().handle_error = handle_error
# gevent.get_hub().handle_system_error = handle_system_error
