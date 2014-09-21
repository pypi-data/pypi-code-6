
import subprocess

from functools import wraps

# gzip decorator
def gzipfiles(func=None, force=False):
    def gzipped_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return gzipped(func(*args, **kwargs), force=force)
        return wrapper
    if func:
        # Decorator declared as @gzipfiles()
        return gzipped_decorator(func)
    else:
        # Decorator declared as @gzipfiles
        def waiting(function):
            return gzipped_decorator(function)
        return waiting

# gunzip decorator
def gunzipfiles(func=None, force=False):
    def gunzipped_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return gunzipped(func(*args, **kwargs), force=force)
        return wrapper
    if func:
        # Decorator declared as @gzipfiles()
        return gunzipped_decorator(func)
    else:
        # Decorator declared as @gzipfiles
        def waiting(function):
            return gunzipped_decorator(function)
        return waiting

def gzipped(paths, force=False):
    return [gzip(path, force=force) for path in paths]

def gunzipped(paths, force=False):
    return [gunzip(path, force=force) for path in paths]

def gzip(path, force=False):
    """gzips a file

    :returns: gzipped name
    """
    command = ["gzip", path]
    if force:
        command.insert(1, "-f")
    if path.endswith(".gz"):
        result = path
    else:
        retcode = subprocess.call(command)
        result = path + ".gz"
    return result

def gunzip(path, force=False):
    """gunzips a file

    :returns: unzipped name
    """
    command = ["gunzip", path]
    if force:
        command.insert(1, "-f")
    if path.endswith(".gz"):
        retcode = subprocess.call(command)
        result = path[:-3]
    else:
        result = path
    return result
