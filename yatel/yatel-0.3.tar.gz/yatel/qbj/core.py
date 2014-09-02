#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""Main logic behind QBJ.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import sys
import json
import traceback

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from yatel import typeconv
from yatel.qbj import functions, schema


#===============================================================================
# CLASS QBJ RESOLVER
#===============================================================================

class QBJResolver(object):
    """Resolver of QBJ calls.

    Parameters
    ----------
    function : dict
        Keys of ``function``:
        
            - ``name`` function to be called.
            - ``args`` positional arguments for function ``name``.
            - ``kwargs`` named arguments for function ``name``.
            
        For further detail on functions arguments see :py:mod:`yatel.qbj.functions`
    context : :py:class:`yatel.db.YatelNetwork`
        Network to execute functions on.

    """

    def __init__ (self, function, context):
        self.function = function
        self.context = context

    def _argument_resolver(self, arg):
        atype = arg["type"]
        value = None
        if "function" in arg:
            function = arg["function"]
            resolver = QBJResolver(function, self.context)
            value = resolver.resolve()
        else:
            value = arg["value"]
        return typeconv.parse({"type": atype, "value": value})

    def resolve(self):
        """Responsible for putting together the call to ``function`` with the
        respective arguments, and return its result.

        """
        name = self.function["name"]
        args = []
        for arg in self.function.get("args", ()):
            result = self._argument_resolver(arg)
            args.append(result)
        kwargs = {}
        for kw, arg in self.function.get("kwargs", {}).items():
            result = self._argument_resolver(arg)
            kwargs[kw] = result
        if "nw" in kwargs:
            return functions.execute(name, *args, **kwargs)
        return functions.execute(name, self.context, *args, **kwargs)


#===============================================================================
# CLASS CORE
#===============================================================================

class QBJEngine(object):
    """Responsible of storing context for QBJ queries, and executes the
    functions required on it.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to be used with the query.

    """

    def __init__(self, nw):
        self.context = nw

    def execute(self, querydict, stacktrace=False):
        """Takes the query in ``querydict`` and executes it after validation of
        it's structure.

        Parameters
        ----------
        querydict : dict
            Dictionary with query in QBJ format.
        stacktrace : bool or False
            True if you want a stacktrace to be generated.

        Returns
        -------
        dict
            Result of the query.
        """
        query_id = None
        function = None
        error = False
        stack_trace = None
        error_msg = ""
        result = None
        try:
            schema.validate(querydict)
            query_id = querydict["id"]
            function = querydict["function"]
            main_resolver = QBJResolver(function, self.context)
            result = typeconv.simplifier(main_resolver.resolve())
        except Exception as err:
            if not query_id and isinstance(querydict, dict):
                query_id = querydict.get("id")
            error = True
            error_msg = unicode(err)
            if stacktrace:
                stack_trace = u"\n".join(
                    traceback.format_exception(*sys.exc_info())
                )
        return {
            "id": query_id, "error": error, "stack_trace": stack_trace,
            "error_msg": error_msg, "result": result
        }


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
