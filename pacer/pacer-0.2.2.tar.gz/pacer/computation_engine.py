import pdb
# encoding: utf-8

import functools
import itertools
import types
import inspect
import os
import glob
import fnmatch

from multiprocessing import cpu_count

from std_logger import get_logger
from dill_multiproc import Pool


class Engine(object):

    pool = None

    @staticmethod
    def set_number_of_processes(n):
        if n < 0:
            n = cpu_count() - n
            n = max(n, 0)
        Engine.pool = Pool(n)


def args_to_str(arg):

    def iterable_to_str(left_delim, ctr, right_delim):
        _i_to_str = lambda t: ", ".join(args_to_str(ti) for ti in t)
        if len(ctr) < 10:
            return left_delim + _i_to_str(ctr) + right_delim
        else:
            return left_delim + _i_to_str(ctr[:5]) + ", ... " + _i_to_str(ctr[-5:]) + right_delim

    if isinstance(arg, tuple):
        return iterable_to_str("(", arg, ")")
    if isinstance(arg, list):
        return iterable_to_str("[", arg, "]")
    if isinstance(arg, set):
        return iterable_to_str("{", sorted(arg), "}")
    if isinstance(arg, dict):
        return iterable_to_str("{", ["%s:%s" % (k, v) for (k, v) in arg.items()], "}")
    return repr(arg)


def _log_fun(logger, job_description, fun, args, kwargs):
    name = fun.__name__
    if len(args) == 1:
        logger.info("%s %s with arg %s and kwargs=%s" % (job_description, name, args_to_str(args),
                                                         args_to_str(kwargs)))
    else:
        logger.info("%s %s with args=%s and kwargs=%s" % (job_description, name, args_to_str(args),
                                                          args_to_str(kwargs)))


class Computation(object):

    cache = dict()

    def __init__(self, f, args, kwargs=None):
        assert Engine.pool is not None, "you forgot to call Computation.set_number_of_processes"
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.job = Engine.pool.apply_async(f, args, kwargs)

    def fetch(self):
        result = self.job.get()
        _log_fun(get_logger(self), "fetched", self.f, self.args, self.kwargs)
        return result

    def __str__(self):
        return "Computation(%s, %s)" % (self.f, map(str, self.args, self.kwargs))


class FinishedComputation(Computation):

    def __init__(self, x):
        self.x = x

    def fetch(self):
        return self.x

    def __str__(self):
        return "FinishedComputation(%s)" % self.x


def files_from(folder, *patterns):
    for f in os.listdir(folder):
        if not patterns or any(fnmatch.fnmatch(f, pattern) for pattern in patterns):
            yield FinishedComputation(os.path.join(folder, f))


def computation_generator(iterator):
    """convert an generator to yield computations which wrap the items
        so we can inject an "pure" generator or a computation stream into
        stream processors.
    """
    for item in iterator:
        if isinstance(item, Computation):
            yield item
        else:
            yield FinishedComputation(item)


def _conv_in_args(args):
    def conv_if_needed(arg):
        if not isinstance(arg, dict):
            if inspect.isgenerator(arg) or hasattr(arg, "__iter__"):
                # make sure that the generator yields Computation instances:
                return computation_generator(arg)
        return computation_generator((arg,))
    return map(conv_if_needed, args)


def apply(inner):
    @functools.wraps(inner)
    def wrapped(*a):
        results = list()
        a = _conv_in_args(a)
        last = (None,) * len(a)
        for arg in itertools.izip_longest(*a):
            aii = tuple(ai.fetch() if ai is not None else ti for (ai, ti) in zip(arg, last))
            last = aii
            _log_fun(get_logger(inner), "start computation", inner, aii, dict())
            result = Computation(inner, aii)
            results.append(result)
        for result in results:
            yield result
    wrapped.inner = inner
    return wrapped


def join(inner):
    @functools.wraps(inner)
    def wrapped(*a):
        results = list()
        a = _conv_in_args(a)
        for args in itertools.product(*a):
            aii = tuple(ai.fetch() for ai in args)
            _log_fun(get_logger(inner), "start computation", inner, aii, dict())
            result = Computation(inner, aii)
            results.append(result)
        for result in results:
            yield result
    wrapped.inner = inner
    return wrapped


def summarize(inner):
    @functools.wraps(inner)
    def wrapped(a):
        a = computation_generator(a)
        result = []
        for ai in a:
            result.append(ai.fetch())
        yield Computation(inner, (result,))
    wrapped.inner = inner
    return wrapped
