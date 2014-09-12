import roadrunner
import os
import hashlib 
import numpy as np

from celery import Celery

app = Celery(
    'tasks',
    backend=os.environ['BROKER_URL'],
    broker=os.environ['BROKER_URL'])
rr = roadrunner.RoadRunner()

currentModel = ''

app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y


@app.task
def rrRun(method, *params):
    if (method is not None):
        if (method == 'load'):
            # Override load method
            newModel = hashlib.md5(params[0].encode('utf-8')).hexdigest()
            global currentModel
            if (newModel == currentModel):
                # Model already loaded
                pass
            else:
                currentModel = newModel
                rr.load(*params)
        elif (isinstance(method, str)):
            result = getattr(rr, method)(*params) 
            if isinstance(result, (np.ndarray, np.generic)):
                result = result.tolist()
            return result 
        else:
            fun = getattr(rr, method.pop(0))
            for m in method:
                fun = getattr(fun, m)
            result = fun(*params)
            if isinstance(result, (np.ndarray, np.generic)):
                result = result.tolist()
            return result 


@app.task
def rrChain(commands):
    results = []
    for command in commands:
        results.append(rrRun(*command))
    return results
