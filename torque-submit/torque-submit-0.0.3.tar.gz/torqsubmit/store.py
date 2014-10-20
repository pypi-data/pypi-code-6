# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import abc
import base64
from tempfile import gettempdir, mkstemp
import pickle
import os

import six


class Mode(object):

    SINGLE_TASK = "SINGLE_TASK"
    """
    Execute a single task in PBS and exit
    """
    MANY_TASKS = "MANY_TASKS"
    """
    Execute many tasks either concurrently on synhroneously. In case of
    concurrent execution concurrency is controlled by python queue.
    """
    PBS_ARRAY = "PBS_ARRAY"
    """
    Execute many tasks either concurrently on synhroneously. In both cases
    concurrency is done by PBS array task.
    """

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)


class StoreProperty(object):

    MODE = "MODE"
    """
    :see:`Mode`
    """
    TASK = "TASK"
    """
    Callable that represents a single task to be executed.
    """
    TASK_COUNT = "TASK_COUNT"
    """
    If there are many tasks here we store task count.
    """
    ENVIORMENT = "ENVIORMENT"
    """
    Bash snippet that sets up the enviorment
    """

    CPUS_PER_TASK = "CPUS_PER_TASK"
    """
    Number of CPUs allocated to each task.
    """

    MAX_TASKS_PER_CHILD = "MAX_TASKS_PER_CHILD"
    """
    In case of ``MANY_TASKS`` mode controlls how often python process will
    be torn down. It will be torn down (and then recreated) after processing
    this many tasks.
    """
    MAP_CHUNKSIZE = "MAP_CHUNKSIZE"
    """
     In case of ``MANY_TASKS`` it can be used to increase number of tasks submitted
     to the python process in one batch.
    """

    @classmethod
    def TASK_NO(self, no):
        return "TASK_{}".format(no)


class StoreNotUsed(Exception):
    pass


class EnvStoreToManyTasks(Exception):
    pass


class TorqeSubmitStore(six.with_metaclass(abc.ABCMeta, object)):

    @property
    @abc.abstractmethod
    def store(self):
        """
        Returns dictionary storing tasks to be submitted
        :return:
        """
        return {}

    @abc.abstractmethod
    def load(self):
        raise StoreNotUsed()

    @classmethod
    @abc.abstractmethod
    def save_store(self, store):
        """
        Saves store to some object
        :param dict store:
        :return: Object representing the store
        """
        pass

    @property
    def mode(self):
        return Mode.fromstring(self.store[StoreProperty.MODE])

    @property
    def map_chunksize(self):
        return self.store.get(StoreProperty.MAP_CHUNKSIZE, 1)

    @property
    def task(self):
        self.__assert_single()
        return self._load_task(self.store[StoreProperty.TASK])

    @property
    def max_tasks_per_child(self):
        return self.store.get(StoreProperty.MAX_TASKS_PER_CHILD, 1)

    @property
    def tasks(self):

        def generator():
            for ii in range(self.task_count):
                yield self.get_task(ii)
        return generator()

    @property
    def tasks_serialized(self):
        def generator():
            for ii in range(self.task_count):
                yield self, ii
        return generator()

    @property
    def cpus_per_task(self):
        return self.store.get(StoreProperty.CPUS_PER_TASK, 1)

    @property
    def task_count(self):
        self.__assert_many()
        return self.store[StoreProperty.TASK_COUNT]

    def get_task(self, no):
        return self._load_task(self.store[StoreProperty.TASK_NO(no)])

    def __assert_single(self):
        assert self.mode == Mode.SINGLE_TASK

    def __assert_many(self):
        assert self.mode in (Mode.MANY_TASKS, Mode.PBS_ARRAY)

    @property
    def _pickle(self):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle

    def _load_task(self, serialized):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle.loads(serialized)

    @classmethod
    def pickle_task(cls, task):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle.dumps(task)

    @classmethod
    def __to_str(cls, v):
        if isinstance(v, str):
            return v.encode('utf-8')
        return v

    @classmethod
    def _filter_store(cls, store):
        if six.PY2:
            return store
        return dict([
            (cls.__to_str(k), cls.__to_str(v)) for k, v in store.items()
        ])



class _EnvDict(dict):
    def __missing__(self, key):
        key = "__PY_T_{}".format(key)
        v = os.environ[key]
        return pickle.loads(base64.b64decode(v))


class EnvStore(TorqeSubmitStore):

    max_number_of_tasks = 10

    @classmethod
    def save_store(cls, store):
        if store[StoreProperty.MODE] in (Mode.MANY_TASKS, Mode.PBS_ARRAY):
            if store[StoreProperty.TASK_COUNT] > cls.max_number_of_tasks:
                raise EnvStoreToManyTasks(
                    "Too much tasks passed to env store, this might cause issues with PBS, so please use other store, "
                    "or remove this check (at your own risk!)s")

        result = {}
        for k, v in store.items():
            result["__PY_T_{}".format(k)] = base64.b64encode(pickle.dumps(v))
        result["__PY_T_{}".format("STORE")] = "ENV"
        return cls._filter_store(result)

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "ENV":
            raise StoreNotUsed()

    @property
    def store(self):
        return _EnvDict()


class FileBasedStore(TorqeSubmitStore):

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "FILE":
            raise StoreNotUsed()
        import pickle
        with open(os.environ['__PY_T_FILE'], 'rb') as f:
            self.__store = pickle.load(f)

    @property
    def store(self):
        return self.__store

    @classmethod
    def set_tepmdir(self, tmpdir):
        os.environ["__PY_T_TEMPDIR"] = tmpdir

    @classmethod
    def get_tempdir(self):
        return os.environ.get("__PY_T_TEMPDIR", gettempdir())

    @classmethod
    def save_store(cls, store):
        import pickle
        opened, file = mkstemp(dir=cls.get_tempdir())
        with open(file, 'wb') as f:
            pickle.dump(store, f)
            f.close()
        return {b"__PY_T_FILE": file.encode("utf-8"), b"__PY_T_STORE": b"FILE"}


def load_store():
    for Store in [FileBasedStore, EnvStore]:
        try:
            s = Store()
            s.load()
            return s
        except StoreNotUsed:
            pass
    print("ENVIRON")
    print(os.environ)
    print("END")
    raise ValueError("Couldn't load any store")