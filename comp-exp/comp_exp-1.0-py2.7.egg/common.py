import inspect
import itertools


def step(prev=None):

    def wrapper(f):
        f._is_step = True
        f._prev_step = prev
        return f

    return wrapper


def arguments(**kwargs):

    def wrapper(f):
        argspec = inspect.getargspec(f)
        assert argspec.args[0] == 'self'
        args = argspec.args[1:]
        if argspec.defaults is not None:
            # don't consider defaults
            args = args[:-len(argspec.defaults)]

        assert all(k in args for k in kwargs)

        f._args = ArgsList(kwargs)
        f._args_prod_values = list(itertools.product(*f._args.values))
        f._args_passable_names = [a for a in args if a not in kwargs]
        return f

    return wrapper


def results(*args, **kwargs):

    def wrapper(f):
        kwargs.update((a, None) for a in args)
        f._results = kwargs
        return f

    return wrapper


class ArgsList(object):

    def __init__(self, kwargs):
        self.kwargs = [(arg, val) if isinstance(val, tuple) else (arg, (None, val))
                       for arg, val in kwargs.items()]

    @property
    def as_triples(self):
        return [(arg, dtype, val)
                for arg, (dtype, val) in self.kwargs]

    @property
    def as_dict(self):
        return {arg: val
                for arg, (dtype, val) in self.kwargs}

    @property
    def as_dtypes_dict(self):
        return {arg: dtype
                for arg, (dtype, val) in self.kwargs}

    @property
    def names(self):
        return [arg
                for arg, (dtype, val) in self.kwargs]

    @property
    def dtypes(self):
        return [dtype
                for arg, (dtype, val) in self.kwargs]

    @property
    def values(self):
        return [val
                for arg, (dtype, val) in self.kwargs]

def get_column_tuples(steps):
    return [('args', step.__name__, argname)
            for step in steps for argname in step._args.names] +\
           [('res', step.__name__, name)
            for step in steps[-1:] for name in step._results.keys()]
