# -*- coding: utf-8 -*-

def update_environ(store):
    import os
    os.environ['PBS_NP'] = str(store.cpus_per_task)

def callable_executor(data):
    store, ii = data
    task = store.get_task(ii)
    task()