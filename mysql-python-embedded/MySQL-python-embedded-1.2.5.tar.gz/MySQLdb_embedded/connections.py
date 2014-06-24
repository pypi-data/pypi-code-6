from contextlib import contextmanager
import importlib
import sys


@contextmanager
def _unload_module(module_name):
    module = importlib.import_module(module_name)
    del sys.modules[module_name]
    yield
    sys.modules[module_name] = module


with _unload_module('MySQLdb.connections'):
    with _unload_module('_mysql'):
        import _mysql_embedded
        sys.modules['_mysql'] = _mysql_embedded

        # this import is a copy, with its _mysql references pointing to _mysql_embedded
        from MySQLdb.connections import *
