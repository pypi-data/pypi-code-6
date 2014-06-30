# -*- coding: utf-8 -*-
"""
Created on 27/06/2014
@author: Carlo Pires <carlopires@gmail.com>
"""
import sys, types, inspect, functools
from importlib import import_module

__version__ = 5

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

def _resolve_type(self, obj):
    if obj is None:
        return NoneType
    elif obj is NotImplemented:
        return NotImplementedType
    elif obj in (True, False):
        return bool
    elif obj.__class__ is Sub:
        return obj
    elif obj.__class__ is tuple:
        return tuple([_resolve_type(self, t) for t in obj])
    elif obj.__class__ is str and '.' in obj:
        if self and obj.startswith('self.'):
            return _resolve_type(self, getattr(self, obj[5:]))
        else:
            return _cached_import(obj)
    else:
        return obj

def _extract_subs(argtypes):
    if argtypes.__class__ is Sub:
        return (argtypes,), ()
    elif argtypes.__class__ is not tuple:
        return (), (argtypes,)
    
    subs, types = [], []
    for argtype in argtypes:
        if argtype.__class__ is Sub:
            subs.append(argtype)
        else:
            types.append(argtype)
    return tuple(subs), tuple(types)

def _validate(self, argname, argvalue, argtype, error_fmt):
    subs, types = _extract_subs(argtype)

    if types and isinstance(argvalue, types):
        return
    
    subs_resolved = []
    for sub in subs:
        subcls = _resolve_type(self, sub.cls)
        subs_resolved.append(subcls)
        if isinstance(argvalue, type) and issubclass(argvalue, subcls):
            return
        if isinstance(argvalue, tuple) and any([issubclass(v, subcls) for v in argvalue]):
            return

    argexpected = []
    if types:
        types = ', '.join([str(t) for t in types])
        argexpected.append('any instance of [{}]'.format(types))
    if subs:
        subs = ', '.join([str(t) for t in subs_resolved])
        argexpected.append('any subclass of {}'.format(subs))
    
    raise TypeCheckError(error_fmt.format(argname=argname, 
                                          argexpected=' or '.join(argexpected), 
                                          argvalue_type=argvalue.__class__.__name__, 
                                          argvalue=argvalue))
        
def _typecheck(f):
    arg_error_fmt = 'Argument "{argname}" expects {argexpected}. However, {argvalue_type} = {argvalue} was found'
    ret_error_fmt = 'Return type was expected to be {argexpected}. However {argvalue_type} = {argvalue} was found'
    
    @functools.wraps(f)
    def decorated(*args, **kws):
        if 'self' in f.__code__.co_varnames:
            self, varnames, varargs = args[0], f.__code__.co_varnames[1:], args[1:] 
        else:
            self, varnames, varargs = None, f.__code__.co_varnames, args
        
        for i, name in enumerate(varnames):
            argtype = _resolve_type(self, f.__annotations__.get(name, NoType))

            if isinstance(argtype, (type, tuple, Sub)):
                if i < len(varargs): 
                    _validate(self, name, varargs[i], argtype, arg_error_fmt)
                elif name in kws:
                    _validate(self, name, kws[name], argtype, arg_error_fmt)
                
        result = f(*args, **kws)
        returntype = _resolve_type(self, f.__annotations__.get('return', NoType))
        
        if isinstance(returntype, (type, tuple, Sub)):
            _validate(self, None, result, returntype, ret_error_fmt)
        
        return result
    return decorated

def typecheck(module_name):
    module_obj = sys.modules[module_name]
    objects = [(0, module_obj, module_obj.__dict__.values())]
    obtyped = []
    while objects:
        level, parent, members = objects.pop()
        for obj in members:
            if obj.__class__ not in (type, types.FunctionType, types.MethodType):
                continue

            if obj.__module__ == module_obj.__name__:
                if hasattr(obj, '__annotations__'):
                    obtyped.append((parent, obj))
                    
                if hasattr(obj, '__dict__'):
                    objects.append((level+1, obj, obj.__dict__.values()))
                
    for obj, func in obtyped:
        setattr(obj, func.__name__, _typecheck(func))
        
    return True

def _caller():
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    caller_args = inspect.getargvalues(caller_frame)
    #caller_annotations = ???
    return caller_name, caller_args

