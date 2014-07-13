"""
This module holds decorators used for simplelog.
"""

import functools
import logging
import sys
import traceback
import pdb as _pdb

from settings import * #TODO: fix to use simplelog
from filters import NullFilter, QuietUnlessExceptionFilter
from simplelog import SIMPLELOG_DEFAULT


def pdb(fn):
    """
    Starts pdb on exception

    #>>> @pdb
    #>>> def func():
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = fn(*args, **kwargs)
        except Exception:
            _type, _value, _tb = sys.exc_info()
            print(_type)
            print(_value)
            _pdb.post_mortem(_tb)
        return res
    return wrapper


def log_exception(fn):
    """
    Logs all exceptions
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = fn(*args, **kwargs)
        except Exception:
            ename, evalue, etb = sys.exc_info()
            print("got an error")
            SIMPLELOG_DEFAULT.error(ename)
            SIMPLELOG_DEFAULT.error(evalue)
            SIMPLELOG_DEFAULT.error("\n".join(traceback.format_tb(etb)))
        return res
    return wrapper



def quiet(dump_on_exception = True):
    """
    Don't show logs

    :param: dump logs on exception, default is True
    """
    logger = SIMPLELOG_DEFAULT
    f = QuietUnlessExceptionFilter()
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            SIMPLELOG_DEFAULT.addFilter(f)
            res = None
            try:
                res = fn(*args, **kwargs)
            except Exception:
                if dump_on_exception:
                    print("Got exception")
                    for r in f.records:
                        msg = "[%s]" % r.levelname
                        msg += " : %s" % r.msg
                        print(msg)
                    print("end of logs")
                raise
            finally:
                SIMPLELOG_DEFAULT.removeFilter(f)
            return res
        return wrapped
    return decorator


def enable(sl):
    "Enables simplelog inside the scope of a function call"
    sl.enable()
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
        print("about to disable simplelog") #DEBUG, #TEMP
        sl.disable()
    return decorator

def disable(sl):
    "disables simplelog inside the scope of a function call"
    sl.disable()
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            #OPTIMIZE: use lambda
            "Just returns the function. Maybe use lambda function?"
            result = function(*args, **kwargs)
            return result
        return wrapper
        sl.enable()
    return decorator


def dump_func(level = None, func_name_only = False, pretty = True):
    """
    This decorate captures the input values of a particular function
    @param:
    level - debug level
    """
    #TODO: make the level actually do something useful
    #TODO: don't return result in func_name_only
    def decorator(function):
        @functools.wraps(function) #propagate docstring to children
        def wrapper(*args, **kwargs):

            log = ""
            func_name = function.__name__
            log += "function: " + func_name + "\n"
            if not func_name_only:
                log += "args: "
                log += ", ".join(["{0!r}".format(a) for a in args])
                log += "\n"
                log += "kwargs: "
                log += ", ".join(["{0!r}".format(a) for a in kwargs])
                log += "\n"
            result = exception = None

            #get result or error
            try:
                result = function(*args, **kwargs)
            except Exception as err:
                exception = err
            finally:
                if exception is None:
                    log += ("result: " + str(result))
                else:
                    import traceback
                    log += ("exception: {0}:{1}".format(type(exception),
                                exception))
                    log += ("{0}".format(traceback.format_exc()))

                if pretty:
                    log += "\n==============\n"

                #Log message
                try:
                    if level:
                        print ("level is " + level)
                    sl = globals()['sl']
                    sl.debug(log)
                except KeyError:
                    sl.quiet()
                    sl.debug(log)
                    pass
                finally:
                    if exception: #FIXME: put somewhere better
                        raise exception
                    return result
        return wrapper
    return decorator
