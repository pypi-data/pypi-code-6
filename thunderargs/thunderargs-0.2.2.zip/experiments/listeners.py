__author__ = 'thunder'


from thunderargs.helpers import wraps


def listen_with(listener):
    def decorator(victim):
        @wraps(victim)
        def wrapper(**kwargs):
            listener(func=victim, **kwargs)
            return victim(**kwargs)
        return wrapper
    return decorator


def logger(func, **kwargs):
    print(func.__name__)
    print(kwargs)