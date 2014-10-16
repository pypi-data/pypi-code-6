import tblib.pickling_support
# allows pickling of basic information from tracebacks:
tblib.pickling_support.install()

import abc
import collections
import dill
import fnmatch
import functools
import itertools
import multiprocessing
import os
import sys
import Queue
import random
import threading
import time
import traceback

from pacer.std_logger import get_logger


class DelayedException(object):

    """store exception for throwing it later.
       we use this for transfering an exception on a worker process to the
       main process.
       only works because we imported and installed tblib above
       """

    def __init__(self, ee):
        self.ee = ee
        __,  __, self.tb = sys.exc_info()

    def re_raise(self):
        raise self.ee, None, self.tb

    def as_string(self):
        return "".join(traceback.format_exception(self.ee, None, self.tb, limit=None))


def eval_pickled(f_s, args_s):
    """ requires function and args serialized with dill, so we can remote execute even lambdas or
    decorated functions or static methods, which 'pure' multiprocssing can not handle"""

    try:
        args = dill.loads(args_s)
    except Exception, e:
        get_logger(eval_pickled).error("got exception when unpickling args: {}".format(e))
        return DelayedException(e)
    try:
        f = dill.loads(f_s)
    except Exception, e:
        get_logger(eval_pickled).error("got exception when unpickling f: {}".format(e))
        return DelayedException(e)
    try:
        if len(args) < 10:
            get_logger(f).info("start {}{} in process {}".format(f.__name__, args, os.getpid()))
        else:
            get_logger(f).info("start {}({} args) in process {}".format(f.__name__, len(args), os.getpid()))
        result = f(*args)
        try:
            n = len(result)
        except:
            n = 0
        if n < 10:
            get_logger(f).info("got result {!r} from process {}".format(result, os.getpid()))
        else:
            get_logger(f).info("got result of len {} from process {}".format(n, os.getpid()))
        return result
    except Exception, e:
        get_logger(f).error("got exception: {}".format(e))
        get_logger(f).exception(e)
        return DelayedException(e)


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
        for arg in enumerated_args:
            if isinstance(arg.value, DelayedException):
                callback(arg)
                return
        new_enumeration, args = unpack(enumerated_args)
        # dill can pickle more function types as pickle module (which underlies
        # multiprocessing) , eg lambdas or static methods, so we transport our computation job
        # serialized as strings, which we deserialize in the remote process again:
        f_s = dill.dumps(f)
        args_s = dill.dumps(args)
        # we use eval_pickled in both cases to make shure we have the same kind of error handling
        # for local and remote execution. this supports debugging.
        if Engine.pool is None:
            result = eval_pickled(f_s, args_s)
            wrap_callback(new_enumeration, callback)(result)
        else:
            Engine.pool.apply_async(eval_pickled, (f_s, args_s),
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

    def put(self, item):
        """this is where computation results are passed to."""
        self._stream.put(item)

    def get_all_in_order(self, do_not_reraise_exceptions=False):
        results = [self.get() for _ in range(self.size())]
        if not do_not_reraise_exceptions:
            for result in results:
                if isinstance(result.value, DelayedException):
                    result.value.re_raise()
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
        return self

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

    def new_function_arguments_for(self, stream_index, item):
        self.data[stream_index].append(item)
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
                    item = stream.get()
                    if isinstance(item.value, DelayedException):
                        self.put(item)
                        return
                    for args in manager.new_function_arguments_for(i, item):
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
        items = []
        stream = self.input_streams[0]
        for i in range(stream.size()):
            item = stream.get()
            if isinstance(item.value, DelayedException):
                self.put(item)
                return
            items.append(item)
        items.sort(key=lambda item: item.number)
        values = [v for __, v in items]
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

    def _collect_data_from_constant_input_streams(self):
        constant_inputs = [None] * len(self.input_streams)
        for i, stream in enumerate(self.input_streams):
            if stream.size() == 1:
                constant_inputs[i] = stream.get()
        return constant_inputs

    def _check_for_any_new_data(self):
        for stream in self.input_streams:
            if stream.size() > 1:
                if not stream.empty():
                    return True
        return False

    def _assemble_function_arguments(self, collected_input_data, cip):
        for i, stream in enumerate(self.input_streams):
            if not stream.empty():
                item = stream.get()
                if item.number not in collected_input_data.keys():
                    collected_input_data[item.number] = cip
                collected_input_data[item.number][i] = item
        for key, arg in collected_input_data.items():
            if all(c is not None for c in arg):
                yield arg
            del collected_input_data[key]

    def _start_computation(self):
        n = 0
        # wait and get the constant args which we need anyway:
        cip = self._collect_data_from_constant_input_streams()
        for item in cip:
            if item is not None:
                if isinstance(item.value, DelayedException):
                    self.put(item)
                    return
        collected_input_data = dict()
        # only constant inputs ?
        if self.size() == 1:
            Engine.run_async(self.f, cip, callback=self.put)
        else:
            while n < self.size():
                avail = self._check_for_any_new_data()
                if avail:
                    for args in self._assemble_function_arguments(collected_input_data, cip):
                        for arg in args:
                            if isinstance(arg, DelayedException):
                                self.put(arg)
                                return
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

    print(sorted(r.get_all_in_order()))
