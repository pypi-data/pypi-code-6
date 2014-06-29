# -*- coding: utf-8 -*-
"""
Created on 27/06/2014
@author: Carlo Pires <carlopires@gmail.com>
"""
import sys, types, inspect, functools
from functools import lru_cache
from importlib import import_module

__version__ = 1.9

class TypeCheckError(Exception): 
    pass

def _caller():
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    caller_args = inspect.getargvalues(caller_frame)
    #caller_annotations = ???
    return caller_name, caller_args

@lru_cache(maxsize=None)
def _cached_import(obj):
    pkg, cls = obj.rsplit('.', 1)
    return getattr(import_module(pkg), cls)

NoType = object()
NoneType = type(None)
NotImplementedType = type(NotImplemented)

def _resolve_type(self, obj):
    if obj is None:
        return NoneType
    elif obj is NotImplemented:
        return NotImplementedType
    elif obj in (True, False):
        return bool
    elif obj.__class__ is tuple:
        return tuple([_resolve_type(self, t) for t in obj])
    elif obj.__class__ is str and '.' in obj:
        if self and obj.startswith('self.'):
            return _resolve_type(self, getattr(self, obj[5:]))
        else:
            return _cached_import(obj)
    else:
        return obj

def _typecheck(f):
    """
    Based on code of David Merts
    @source: http://code.activestate.com/recipes/users/4173018/
    """
    arg_error_fmt = 'Argument {} expects an instance of {}, {} found'
    ret_error_fmt = 'Return type is expected to be {}, {} found'
    
    @functools.wraps(f)
    def decorated(*args, **kws):
        if 'self' in f.__code__.co_varnames:
            self, varnames, varargs = args[0], f.__code__.co_varnames[1:], args[1:] 
        else:
            self, varnames, varargs = None, f.__code__.co_varnames, args
        
        for i, name in enumerate(varnames):
            argtype = _resolve_type(self, f.__annotations__.get(name, NoType))

            # Only check if annotation exists and it is as a type
            if isinstance(argtype, (type, tuple)):
                # First len(varargs) are positional, after that keywords
                if i < len(varargs) and not isinstance(varargs[i], argtype):
                    raise TypeCheckError(arg_error_fmt.format(name, argtype, varargs[i].__class__))
                elif name in kws and not isinstance(kws[name], argtype):
                    raise TypeCheckError(arg_error_fmt.format(name, argtype, kws[name].__class__))
                
        result = f(*args, **kws)
        returntype = _resolve_type(self, f.__annotations__.get('return', NoType))
        
        if isinstance(returntype, (type, tuple)) and not isinstance(result, returntype):
            raise TypeCheckError(ret_error_fmt.format(returntype, result.__class__))
        
        return result
    return decorated

def typecheck(module_name):
    module_obj = sys.modules[module_name]
    objects = [(0, module_obj, module_obj.__dict__.values())]
    obtyped = []
    while objects:
        level, parent, members = objects.pop()
        for obj in members:
            if obj.__class__ is types.ModuleType:
                continue
            
            if hasattr(obj, '__annotations__'):
                obtyped.append((parent, obj))
                
            if hasattr(obj, '__dict__'):
                objects.append((level+1, obj, obj.__dict__.values()))
                
    for obj, func in obtyped:
        setattr(obj, func.__name__, _typecheck(func))
        
    return True

