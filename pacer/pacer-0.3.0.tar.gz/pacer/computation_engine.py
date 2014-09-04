import pdb
import abc
import time
import os
import random
import fnmatch
import multiprocessing
import Queue
import itertools
import functools

import dill

from pacer.std_logger import get_logger


def remote_eval(f_s, args_s):
    """ requires function and args serialized with dill, so we can remote execute even lambdas or
    decorated functions or static methods, which 'pure' multiprocssing can not handle"""

    args = dill.loads(args_s)
    f = dill.loads(f_s)
    get_logger(f).info("start {}{} in process {}".format(f.__name__, args, os.getpid()))
    try:
        result = f(*args)
        get_logger(f).info("got result {} from process {}".format(result, os.getpid()))
        return result
    except Exception, e:
        get_logger(f).error("got exception: {}".format(e))
        args_s = ", ".join("{}".format(ai) for ai in args)
        return Exception(e.message + ", source: {}({})".format(f.__name__, args_s))


class EnumeratedItem(object):

    def __init__(self, number, value):
        self.number = number
        self.value = value

    def __iter__(self):
        return iter((self.number, self.value))


def unpack(enumerated_args):
    new_enumeration = tuple(i for (i, __) in enumerated_args)
    if len(new_enumeration) == 1:
        new_enumeration = new_enumeration[0]
    argument = tuple(a for (__, a) in enumerated_args)
    return new_enumeration, argument


def wrap_callback(new_enumeration, callback):
    """creates a new callback which builds a EnumeratedItem from the reult """
    def new_callback(result):
        callback(EnumeratedItem(new_enumeration, result))
    return new_callback


class Engine(object):

    pool = None

    @staticmethod
    def set_number_of_processes(n):
        if n is None:
            Engine.pool = None
            return
        if n < 0:
            n = multiprocessing.cpu_count() - n
            n = max(n, 0)
        if n > 0:
            Engine.pool = multiprocessing.Pool(n)
        elif n == 0:
            Engine.pool = None
        else:
            raise Exception("can not set number of processes to %d" % n)

    @staticmethod
    def run_async(f, enumerated_args, callback):
        """ f is not implemented for handling enumerated items, so we exctract the items
        and construct a 'new enumeration' for the result.
        This is needed in order to ensure that the final result of the computations have
        a fixed order although their computation order might be different due to the
        concurrent processing."""
        assert all(isinstance(arg, EnumeratedItem) for arg in enumerated_args)
        new_enumeration, args = unpack(enumerated_args)
        if Engine.pool is None:
            wrap_callback(new_enumeration, callback)(f(*args))
        else:
            # dill can pickle more function types as pickle module (which underlies
            # multiprocessing) , eg lambdas or static methods, so we transport our computation job
            # serialized as strings, which we deserialize in the remote process again:
            f_s = dill.dumps(f)
            args_s = dill.dumps(args)
            Engine.pool.apply_async(remote_eval,
                                    (f_s, args_s),
                                    callback=wrap_callback(new_enumeration, callback))


class DataStream(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._stream = Queue.Queue()

    def empty(self):
        return self._stream.empty()

    def get(self):
        return self._stream.get()

    def size(self):
        return self._size

    def put(self, value):
        self._stream.put(value)

    def get_all_in_order(self):
        results = [self.get() for _ in range(self.size())]
        results.sort(key=lambda en_item: en_item.number)
        return [item.value for item in results]


class Source(DataStream):

    def __init__(self, source):
        super(Source, self).__init__()
        self._size = len(source)
        for i, item in enumerate(source):
            self.put(EnumeratedItem(i, item))

    def __iter__(self):
        while not self.empty():
            yield self.get().value


def files_from(folder, *patterns):
    files = []
    for f in os.listdir(folder):
        if not patterns or any(fnmatch.fnmatch(f, pattern) for pattern in patterns):
            files.append(os.path.join(folder, f))
    return Source(files)


class _ConstantSource(Source):

    def __init__(self, value):
        super(ConstantSource, self).__init__([value])


class Computation(DataStream):

    def __init__(self, f, inputs):
        super(Computation, self).__init__()
        self.f = f
        self.input_streams = self._setup_inputs(inputs)
        self._size = self.compute_size()

    def _setup_inputs(self, inputs):
        streams = []
        for input_ in inputs:
            stream = input_
            if not isinstance(input_, DataStream):
                if isinstance(input_, (tuple, list)):
                    stream = Source(input_)
                else:
                    stream = Source((input_,))
            streams.append(stream)
        return streams

    def start_computations(self):
        """
        starts computations at leafs first then up to the root
        """
        for stream in self.input_streams:
            if isinstance(stream, Computation):
                stream.start_computations()
        self._start_computation()

    @abc.abstractmethod
    def compute_size(self):
        pass

    @abc.abstractmethod
    def _start_computation(self):
        pass


class _UpdateManagerForJoin(object):

    """ manages input data from sources which might come in in arbitrary order.  handles
    incremental generation of input_streams for computations.  """

    def __init__(self, input_streams):
        self.seen = set()
        # a list of collected data per stream:
        self.data = [list() * a.size() for a in input_streams]

    def new_function_arguments_for(self, stream_index, value):
        self.data[stream_index].append(value)
        # cross product over all indices of available data:
        sizes = [len(v) for v in self.data]
        for perm in itertools.product(*(range(size) for size in sizes)):
            if perm not in self.seen:
                args = tuple(self.data[j][pi] for j, pi in enumerate(perm))
                yield args
                self.seen.add(perm)

    def input_data_pending(self, size):
        return len(self.seen) < size


class JoinComputation(Computation):

    def compute_size(self):
        return reduce(lambda x, y: x * y, (a.size() for a in self.input_streams))

    def _start_computation(self):

        manager = _UpdateManagerForJoin(self.input_streams)
        while manager.input_data_pending(self.size()):
            started_computation = False
            for i, stream in enumerate(self.input_streams):
                if not stream.empty():
                    val = stream.get()
                    for args in manager.new_function_arguments_for(i, val):
                        Engine.run_async(self.f, args, callback=self.put)
                        started_computation = True
            if not started_computation:
                time.sleep(0.001)


class SummarizeComputation(Computation):


    def __init__(self, f, inputs):
        assert len(inputs) == 1, "reduce computations only accept one input stream"
        super(SummarizeComputation, self).__init__(f, inputs)

    def compute_size(self):
        return 1

    def _start_computation(self):
        values = []
        stream = self.input_streams[0]
        for i in range(stream.size()):
            values.append(stream.get())
        values.sort(key=lambda item: item.number)
        values = [v for __, v in values]
        arg = EnumeratedItem(0, values)
        Engine.run_async(self.f, (arg,), callback=self.put)


class ZipComputation(Computation):

    """either input_streams provide all n inputs or one fixed input. The latter is managed by
    ConstantSource class.
    """

    def compute_size(self):
        sizes = set(s.size() for s in self.input_streams)
        if 1 in sizes:
            sizes.remove(1)
        if len(sizes) > 1:
            msg = "allow ownly sources with same sized outputs or constant constant source"
            raise Exception(msg)
        if len(sizes) == 1:
            return sizes.pop()
        # sizes has size 0 means: we only had inputs of size 1
        return 1

    def _get_constant_inputs(self):
        constant_inputs = [None] * len(self.input_streams)
        for i, stream in enumerate(self.input_streams):
            if stream.size() == 1:
                constant_inputs[i] = stream.get()
        return constant_inputs

    def _check_for_new_data(self):
        for stream in self.input_streams:
            if stream.size() > 1:
                if stream.empty():
                    return False
        return True

    def _assemble_function_arguments(self, constant_inputs):
        args = [None] * len(self.input_streams)
        for i, stream in enumerate(self.input_streams):
            if stream.size() == 1:
                args[i] = constant_inputs[i]
            else:
                args[i] = stream.get()
        return tuple(args)

    def _start_computation(self):
        n = 0
        # wait and get the constant args which we need anyway:
        constant_inputs = self._get_constant_inputs()
        while n < self.size():
            avail = self._check_for_new_data()
            if avail:
                args = self._assemble_function_arguments(constant_inputs)
                Engine.run_async(self.f, args, callback=self.put)
                n += 1
            else:
                time.sleep(0.001)


def apply(inner):
    @functools.wraps(inner)
    def wrapped(*args):
        return ZipComputation(inner, args)
    wrapped.inner = inner
    return wrapped


def join(inner):
    @functools.wraps(inner)
    def wrapped(*args):
        return JoinComputation(inner, args)
    wrapped.inner = inner
    return wrapped


def summarize(inner):
    @functools.wraps(inner)
    def wrapped(*args):
        return SummarizeComputation(inner, args)
    wrapped.inner = inner
    return wrapped


if __name__ == "__main__":

    @join
    def add(*args):
        time.sleep(0.5 * random.random())
        return sum(args)

    @apply
    def inc(x, config=dict()):
        time.sleep(0.5 * random.random())
        return x + config.get("increment", 1)

    @summarize
    def avg(values):
        return float(sum(values)) / len(values)

    Engine.set_number_of_processes(7)
    N = 3

    s1 = range(N)
    s2 = range(1, N + 1)
    r = add(0, 1, s1)

    r = inc(avg(inc(add(0, 1, add(inc(s1), inc(s2), inc(7))), dict(increment=2))))

    r.start_computations()

    print sorted(r.get_all_in_order())
