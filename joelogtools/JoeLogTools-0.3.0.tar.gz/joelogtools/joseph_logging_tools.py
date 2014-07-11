
# Name: joseph_logging_tools.py
# Author: Joseph Gordon
# Date Created: Thursday July 3, 2014

import logging
from types import FunctionType

def starting_ending_decorator(some_func):
    """This function decorates each method within a class with the debug level
    logging event 'starting <method_name>' before method call, and the debug
    level logging event 'ending <mehod_name>' after method call.
    """
    def inner(*args, **kwargs):
        self = args[0]
        self.logger.debug('starting %s' % (some_func.__name__))
        result = some_func(*args, **kwargs)
        self.logger.debug('ending %s' % (some_func.__name__))
        return result
    return inner

def init_starting_ending_decorator(some_func):
    """This function decorater is similar to starting_ending_decorator(func).
    However the debug level event 'starting <method_name>' belongs to the root
    logger instead of the class logger. At this logging event no Logger object
    has been instantiated within the class.

    """
    def inner(*args, **kwargs):
        self = args[0]
        logging.debug('starting %s' % (some_func.__name__))
        result = some_func(*args, **kwargs)
        self.logger.debug('ending %s' % (some_func.__name__))
        return result
    return inner

def init_logging_wrapper(some_func):
    """This function wraps the __init__ method of a class which utilizes
    LoggingMetaClass as a metaclass. It ensures that an instance of Logger
    is present within the class. 
    """
    def class_wrapped_init(*args, **kwargs):
        self = args[0]
        self.logger = logging.getLogger(self.__class__.__name__)
        result = some_func(*args, **kwargs)
        return result
    return class_wrapped_init
       
        
class LoggingMetaClass(type):
    """The metaclass ensures that each customer class has a Logger
    object, and that each method is decorated with debug level logging events
    which indicate the start and end of the method.
    """
    def __new__(cls, name, bases, dct):
                
        for attr, attrval in dct.items():                      
            if attr == '__init__':
                dct[attr] = init_logging_wrapper(dct[attr])
                dct[attr] = init_starting_ending_decorator(dct[attr])
                break
                
        for attr, attrval in dct.items():
            if type(attrval) is FunctionType and attr != '__init__' :
                dct[attr] = starting_ending_decorator(attrval)              
                                                
        return type.__new__(cls, name, bases, dct)

    

    


  
  
