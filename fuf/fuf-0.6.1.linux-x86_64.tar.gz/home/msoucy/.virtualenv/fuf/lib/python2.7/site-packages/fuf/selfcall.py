'''
selfcall.py
Matt Soucy

Simple decorators related to "self-calling" things
'''

def mainfunc(func):
    if func.__module__ == '__main__': func()
    return func

def SelfInit(*args, **kwargs):
    # Special-case to handle decorating without args
    # Yes, this fails when you want to pass a callable
    # as the only argument. There doesn't seem to be a convenient
    # way to handle that at this time
    if len(args) == 1 and not kwargs and hasattr(args[0], '__call__'):
        return SelfInit()(args[0])
    def _wrap(func):
        return func(*args, **kwargs)
    return _wrap
