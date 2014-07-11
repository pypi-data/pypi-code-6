
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
    LoggingMetaClass as a metaclass. It passes an instance of Logger as
    the first argument to the LoggingAdapter class. The second argument
    passed to the LoggingAdapter class is a dictionary containing both
    class and instance properties. All logging events are calls to
    LoggingAdapter. 
    """
    def class_wrapped_init(*args, **kwargs):
        self = args[0]
        logger = logging.getLogger(self.__class__.__name__)
        extra = dict(
            class_properties = self.__class__.__dict__,
            instance_properties = self.__dict__
        )
        #extra = {'Piggly': 'Wiggly'}
        self.logger = LoggingAdapter(logger, extra)
        result = some_func(*args, **kwargs)
        return result
    return class_wrapped_init


class LoggingAdapter(logging.LoggerAdapter):
    """This is a subclass of the LoggerAdapter class located in the Python
    logging library. It is used to append class and instance properties
    to logging events.
    """
    def process(self, msg, kwargs):
        return '%s  |%s|' % (msg, [self.extra]), kwargs       
        
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

    

    


  
  
