# -*- coding: utf-8 -*-
"""
Created on 27/06/2014
@author: Carlo Pires <carlopires@gmail.com>
"""
import sys, types, inspect, functools

__version__ = 1.0

class TypeCheckError(Exception): 
    pass

def _caller():
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    caller_args = inspect.getargvalues(caller_frame)
    #caller_annotations = ???
    return caller_name, caller_args

def _typecheck(f):
    """
    Based on code of David Merts
    @source: http://code.activestate.com/recipes/users/4173018/
    """
    arg_error_fmt = 'Argument {} expects an instance of {}, {} found'
    ret_error_fmt = 'Return type is expected to be {}, {} found'
    NoneType = type(None)
    
    @functools.wraps(f)
    def decorated(*args, **kws):
        
        for i, name in enumerate(f.__code__.co_varnames):
            if name == 'self':
                continue
            
            argtype = f.__annotations__.get(name)

            # make developer's life easy with None type            
            if argtype is None:
                argtype = NoneType
            
            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional, after that keywords
                if i < len(args) and not isinstance(args[i], argtype):
                    raise TypeCheckError(arg_error_fmt.format(name, argtype, args[i].__class__))
                elif name in kws and not isinstance(kws[name], argtype):
                    raise TypeCheckError(arg_error_fmt.format(name, argtype, kws[name].__class__))
                
        result = f(*args, **kws)
        returntype = f.__annotations__.get('return')
        
        # make developer's life easy with None type            
        if returntype is None:
            returntype = NoneType
        
        if isinstance(returntype, type) and not isinstance(result, returntype):
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

