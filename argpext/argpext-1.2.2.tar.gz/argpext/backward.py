"""

Argpext: Hierarchical argument processing based on argparse.

Copyright (c) 2012,2014 by Alexander V. Shirokov. This material
may be distributed only subject to the terms and conditions
set forth in the Open Publication License, v1.0 or later
(the latest version is presently available at
http://www.opencontent.org/openpub ).


"""

import argpext
from argpext import *


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Backward compatibility with argpext version 1.1           !!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Function(tasks.Task):
    def __init__(self,*args,**kwds):
        warnings.warn("Please rename all 'argpext.Function' into 'argpext.Task'. "\
                      "The support for 'argpext.Function' may terminate starting from argpext Version 2.0"
                      , UserWarning)
        tasks.Task.__init__(self,*args,**kwds)

class Unit(object):
    "Value unit for Categorical variables."
    def __init__(self,value,help=None,callable=False):
        warnings.warn("Classes Categorical and Unit are now deprecated. "\
                          "Please use the new argpext.KeyWords class and standard pythons map to achieve the identical functionality."\
                          "The support for Unit may terminate starting from argpext Version 2.0"
                      , UserWarning)
        self._value = value
        assert(isinstance(help,(str,type(None),) ))
        self._help = help
        self._callable = callable
        assert(isinstance(callable,bool))
    def evaluate(self):
        return self._value() if self._callable else self._value


class Categorical(object):
    "Categorical variable type."""
    def __init__(self,mapping=(),typeothers=None):
        warnings.warn("Classes Categorical and Unit are now deprecated. "\
                          "Please use the new argpext.KeyWords class and standard pythons map to achieve identical effects."\
                          "The support for Unit may terminate starting from argpext Version 2.0"
                      , UserWarning)
        L = []
        count = 0
        for q in mapping:
            count += 1
            if isinstance(q,str): 
                item = (q, Unit(value=q))
            elif isinstance(q,(list,tuple)):

                if len(q) != 2: 
                    raise InitializationError('invalid size %d for %s item number %d' % ( len(q), type(q).__name__, count ) )

                if not isinstance(q[1],Unit):
                    q = [q[0],Unit(value=q[1])]
                item = q
            else:
                raise InitializationError('invalid type (%s) for mapping item number %d.' % ( type(q).__name__, count ) )
            L += [ item ]

        self.__dict = collections.OrderedDict(L)
        self.__typeothers = typeothers

    def __str__(self):
        K = []
        for key,choice in self.__dict.items():
            K += [key]

        q = self.__typeothers
        if q is not None:
            K += ['%s()' % q.__name__ ]

        return '{%s}' % ( '|'.join(K) )

    def __call__(self,key):
        "Finds and returns value associated with the given key."
        if key in self.__dict:
            return self.__dict[key].evaluate()
        else:
            if self.__typeothers is None:
                raise KeyEvaluationError('unmatched key: "%s".' % (key) )
            else:
                return self.__typeothers(key)




