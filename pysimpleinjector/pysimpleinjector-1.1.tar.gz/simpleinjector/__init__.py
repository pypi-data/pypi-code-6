from functools import wraps

import inspect


class InjectorConfiguration:

    """Class with static methods to configure the @inject decorator.

    Injection works with a very simply principle, this class contains
    key=>value mappings of arguments. When methods decorated with the @inject
    decorator are called, if they have arguments named equal to any of the
    keys, then the corresponding value is injected as a argument value.

    This class contains two types of arguments: static and runtime. Static
    arguments are injected as they are to decorated methods. Runtime arguments
    are actually functions that are executed and their return value are
    injected.
    """

    static_arg = {}
    runtime_arg_pre = {}
    runtime_arg_post = {}

    @staticmethod
    def add_static_arg(name, param):
        """Adds a static argument name."""
        InjectorConfiguration.static_arg[name] = param

    @staticmethod
    def get_static_arg(name):
        """Returns the injectable value of argument ``name``."""
        return InjectorConfiguration.static_arg[name]

    @staticmethod
    def list_static_arg():
        """Returns a list of all the argument names for static arguments"""
        return list(InjectorConfiguration.static_arg.keys())

    @staticmethod
    def add_runtime_arg(name, pre, post=None):
        """Adds a new runtime argument.

        The value returned by the function ``pre`` is injected as a keyword
        arguments ``name`` to any decorted functions. ``post`` is executed
        after the decorated function returns.
        ``post`` will only be executed if the decorated function had an
        argument named ``name``. ``post`` will receive the injected value as a
        single, positional argument.

        :arg string name: The name of an argument where a value should be
            injected.
        :arg function pre: A function who's return value is injected.
        :arg function post: A function that's executed after the decorated
            function returns.
        """
        assert(pre is not None)
        InjectorConfiguration.runtime_arg_pre[name] = pre
        InjectorConfiguration.runtime_arg_post[name] = post

    @staticmethod
    def get_runtime_arg(name):
        """Returns the functions associated with runtime argument ``name``.

        The first function is the one that generates the value that should be
        injected to the decorated function. The second function should be
        called after the decorated function returns.
        """
        pre = InjectorConfiguration.runtime_arg_pre[name]
        post = InjectorConfiguration.runtime_arg_post[name]
        return pre, post

    @staticmethod
    def list_runtime_args():
        """Returns a list of all the argument names for runtime arguments"""
        return list(InjectorConfiguration.runtime_arg_pre.keys())


def inject(method):
    """
    Injects kwargs for which there is a matching args name.

    Register what's passed by using Injector.add_param().
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        post_runtime_funcs = {}

        for arg_name in InjectorConfiguration.list_static_arg():
            if arg_name in inspect.getargspec(method).args:
                value = InjectorConfiguration.get_static_arg(arg_name)
                kwargs[arg_name] = value

        for arg_name in InjectorConfiguration.list_runtime_args():
            if arg_name in inspect.getargspec(method).args:
                funcs = InjectorConfiguration.get_runtime_arg(arg_name)
                value = funcs[0]()
                post_runtime_funcs[funcs[1]] = value
                kwargs[arg_name] = value

        result = method(self, *args, **kwargs)

        for func, value in post_runtime_funcs.items():
            if func is not None:
                func(value)

        return result

    return wrapper
