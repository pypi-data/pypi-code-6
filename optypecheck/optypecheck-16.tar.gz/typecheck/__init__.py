"""
@author: Carlo Pires <carlopires@gmail.com>
"""
import os
import sys
import inspect
import functools
from types import FunctionType, MethodType
from importlib import import_module
from collections import deque

DEBUG = os.environ.get('OPTYPECHECKDEBUG', False)
DEBUG_OUTPUT = None

if DEBUG and DEBUG_OUTPUT is None:
    DEBUG_OUTPUT = open(DEBUG, 'a+')


class TypeCheckError(Exception):
    pass

cache = {}


def _cached_import(obj):
    try:
        return cache[obj]
    except KeyError:
        pkg, cls = obj.rsplit('.', 1)
        cache[obj] = getattr(import_module(pkg), cls)
        return cache[obj]

NoType = object()
NoneType = type(None)
NotImplementedType = type(NotImplemented)


class Sub:
    def __init__(self, cls):
        self.cls = cls


def _getattr(obj, name):
    value = None
    for name in name.split('.'):
        value = getattr(obj, name)
        obj = value
    return value


def _resolve_type(owner, obj):
    if obj.__class__ is Sub:
        return obj
    elif obj.__class__ is tuple:
        return tuple([_resolve_type(owner, t) for t in obj])
    elif obj.__class__ is str and '.' in obj:
        if owner and obj.startswith(('self.', 'cls.')):
            return _resolve_type(owner, _getattr(owner, obj[5:]))
        else:
            return _cached_import(obj)
    else:
        return obj

TupleType = type(tuple())


def _extract_subs(argtypes):
    if argtypes.__class__ is Sub:
        return (argtypes,), ()
    elif argtypes.__class__ is not TupleType:
        return (), (argtypes,)

    subs, types = [], []
    for argtype in argtypes:
        if argtype.__class__ is Sub:
            subs.append(argtype)
        else:
            types.append(argtype)
    return tuple(subs), tuple(types)


def _validate(owner, argname, argvalue, argtype, error_fmt):
    subs, types = _extract_subs(argtype)

    def _debug(v):
        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('\n\t{} matched {}'.format(argvalue.__class__,
                                                          v))

    try:
        if types and isinstance(argvalue, types):
            _debug(types)
            return
    except TypeError as error:
        raise TypeError('{}\n\t{}'.format(error, types))

    subs_resolved = []
    for sub in subs:
        subcls = _resolve_type(owner, sub.cls)
        subs_resolved.append(subcls)
        if isinstance(argvalue, type) and issubclass(argvalue, subcls):
            _debug(subcls)
            return
        if isinstance(argvalue, tuple) and any([issubclass(v, subcls)
                                                for v in argvalue]):
            _debug(subcls)
            return

    argexpected = []
    if types:
        types = ', '.join([str(t) for t in types])
        argexpected.append('any instance of [{}]'.format(types))
    if subs:
        subs = ', '.join([str(t) for t in subs_resolved])
        argexpected.append('any subclass of {}'.format(subs))

    cls_name = argvalue.__class__.__name__

    raise TypeCheckError(error_fmt.format(argname=argname,
                                          argexpected=' or '.join(argexpected),
                                          argvalue_type=cls_name,
                                          argvalue=argvalue))


def _typecheck(f):
    arg_error_fmt = 'Argument "{argname}" expects {argexpected}. ' \
                    'However, {argvalue_type} = {argvalue} was found'

    ret_error_fmt = 'Return type was expected to be {argexpected}. ' \
                    'However {argvalue_type} = {argvalue} was found'

    @functools.wraps(f)
    def decorated(*args, **kws):
        if 'self' in f.__code__.co_varnames or 'cls' in f.__code__.co_varnames:
            owner, varnames, varargs = \
                args[0], f.__code__.co_varnames[1:], args[1:]
        else:
            owner, varnames, varargs = None, f.__code__.co_varnames, args

        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('\n')
            DEBUG_OUTPUT.write('-'*40)

        for i, name in enumerate(varnames):
            argtype = _resolve_type(owner, f.__annotations__.get(name, NoType))

            if isinstance(argtype, (type, tuple, Sub)):
                if i < len(varargs):
                    if DEBUG_OUTPUT:
                        fmt = '\nINPUT {}.{}(arg={}) -> '
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__, i))

                        DEBUG_OUTPUT.write('{}'.format(argtype))

                    _validate(owner, name, varargs[i], argtype, arg_error_fmt)

                elif name in kws:
                    if DEBUG_OUTPUT:
                        fmt = '\nINPUT {}.{}(kwarg={}) -> '
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__,
                                                      name))

                        DEBUG_OUTPUT.write('{}'.format(argtype))

                    _validate(owner, name, kws[name], argtype, arg_error_fmt)
            else:
                if DEBUG_OUTPUT:
                    if i < len(varargs):
                        fmt = '\nNO TYPECHECK {}.{}(arg={}) -> {}'
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__, i,
                                                      argtype))
                    elif name in kws:
                        fmt = '\nNO TYPECHECK {}.{}(kwarg={}) -> {}'
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__,
                                                      name, argtype))

        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('\n')

        result = f(*args, **kws)
        returntype = _resolve_type(owner,
                                   f.__annotations__.get('return', NoType))

        if isinstance(returntype, (type, tuple, Sub)):
            if DEBUG_OUTPUT:
                DEBUG_OUTPUT.write('\nOUTPUT {}.{} -> '.format(f.__module__,
                                                               f.__name__))
                DEBUG_OUTPUT.write('{}'.format(returntype))

            _validate(owner, None, result, returntype, ret_error_fmt)
        else:
            if DEBUG_OUTPUT:
                fmt = '\nNO TYPECHECK OUTPUT {}.{}'
                DEBUG_OUTPUT.write(fmt.format(f.__module__, f.__name__))

        return result
    return decorated


def _typecheck_coro(f):
    arg_error_fmt = 'Argument "{argname}" expects {argexpected}. ' \
                    'However, {argvalue_type} = {argvalue} was found'

    ret_error_fmt = 'Return type was expected to be {argexpected}. ' \
                    'However {argvalue_type} = {argvalue} was found'

    @functools.wraps(f)
    def decorated(*args, **kws):
        if 'self' in f.__code__.co_varnames or 'cls' in f.__code__.co_varnames:
            owner, varnames, varargs = \
                args[0], f.__code__.co_varnames[1:], args[1:]
        else:
            owner, varnames, varargs = None, f.__code__.co_varnames, args

        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('\n')
            DEBUG_OUTPUT.write('-'*40)

        for i, name in enumerate(varnames):
            argtype = _resolve_type(owner, f.__annotations__.get(name, NoType))

            if isinstance(argtype, (type, tuple, Sub)):
                if i < len(varargs):
                    if DEBUG_OUTPUT:
                        fmt = '\nINPUT {}.{}(arg={}) -> '
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__, i))

                        DEBUG_OUTPUT.write('{}'.format(argtype))

                    _validate(owner, name, varargs[i], argtype, arg_error_fmt)

                elif name in kws:
                    if DEBUG_OUTPUT:
                        fmt = '\nINPUT {}.{}(kwarg={}) -> '
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__,
                                                      name))

                        DEBUG_OUTPUT.write('{}'.format(argtype))

                    _validate(owner, name, kws[name], argtype, arg_error_fmt)
            else:
                if DEBUG_OUTPUT:
                    if i < len(varargs):
                        fmt = '\nNO TYPECHECK {}.{}(arg={}) -> {}'
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__, i,
                                                      argtype))
                    elif name in kws:
                        fmt = '\nNO TYPECHECK {}.{}(kwarg={}) -> {}'
                        DEBUG_OUTPUT.write(fmt.format(f.__module__,
                                                      f.__name__,
                                                      name, argtype))

        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('\n')

        result = (yield from f(*args, **kws))
        returntype = _resolve_type(owner,
                                   f.__annotations__.get('return', NoType))

        if isinstance(returntype, (type, tuple, Sub)):
            if DEBUG_OUTPUT:
                DEBUG_OUTPUT.write('\nOUTPUT {}.{} -> '.format(f.__module__,
                                                               f.__name__))
                DEBUG_OUTPUT.write('{}'.format(returntype))

            _validate(owner, None, result, returntype, ret_error_fmt)
        else:
            if DEBUG_OUTPUT:
                fmt = '\nNO TYPECHECK OUTPUT {}.{}'
                DEBUG_OUTPUT.write(fmt.format(f.__module__, f.__name__))

        return result
    return decorated


def typecheck(module_name):
    module_obj = sys.modules[module_name]
    objects = deque()
    objects.append((0, module_obj, module_obj.__dict__.values()))
    obtyped = set()
    while objects:
        level, parent, members = objects.popleft()
        for obj in members:
            if DEBUG_OUTPUT:
                m = '{}'.format(obj.__module__) \
                    if hasattr(obj, '__module__') else ''
                c = '{}'.format(obj)
                n = obj.__class__

                DEBUG_OUTPUT.write('\nFOUND {}.{}(type={})'.format(m, c, n))

#             if obj.__class__ not in (type, FunctionType, MethodType):
#                 if DEBUG_OUTPUT:
#                     DEBUG_OUTPUT.write(' (skipped)')
#                 continue

            if hasattr(obj, '__module__') and \
                    obj.__module__ == module_obj.__name__:

                if hasattr(obj, '__annotations__'):
                    obtyped.add((parent, obj))

                if hasattr(obj, '__dict__'):
                    objects.append((level+1, obj, obj.__dict__.values()))

    if DEBUG_OUTPUT:
        DEBUG_OUTPUT.write('\n')

    for obj, func in obtyped:
        if DEBUG_OUTPUT:
            DEBUG_OUTPUT.write('TYPECHECKED {}.{}\n'.format(func.__module__,
                                                            func.__name__))
        if hasattr(func, '_is_coroutine'):
            setattr(obj, func.__name__, _typecheck_coro(func))
        else:
            setattr(obj, func.__name__, _typecheck(func))

    if DEBUG_OUTPUT:
        DEBUG_OUTPUT.write('\n')

    return True


def _caller():
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    caller_args = inspect.getargvalues(caller_frame)
#    caller_annotations = ???
    return caller_name, caller_args
