# -*- coding: utf-8 -*-
import multiprocessing
import os
import sys

from torqsubmit.store import load_store, Mode, TorqeSubmitStore
from torqsubmit._misc import callable_executor, update_environ


# for k, v in os.environ.items():
#     if "__PY_T" in k:
#         print(k, v)

store = load_store()

assert isinstance(store, TorqeSubmitStore)


# print (store.store)

if store.mode == Mode.SINGLE_TASK:
    store.task()
    sys.exit(0)

if store.mode == Mode.PBS_ARRAY:
    task = store.get_task(os.environ.get("PBS_ARRAYID"))
    task()
    sys.exit(0)

cpus = int(os.environ.get("PBS_NP", 1))
tasks = store.tasks

if cpus == 1:
    for t in tasks:
        t()
else:
    processes = int(cpus / store.cpus_per_task)
    p = multiprocessing.Pool(processes, initializer=update_environ, initargs=[store], maxtasksperchild=store.max_tasks_per_child)
    p.map(callable_executor, store.tasks_serialized, chunksize=store.map_chunksize)
    p.close()
    p.join()
