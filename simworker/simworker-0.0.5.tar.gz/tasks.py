import roadrunner
import os
import md5

from celery import Celery

app = Celery(
    'tasks',
    backend=os.environ['BROKER_URL'],
    broker=os.environ['BROKER_URL'])
rr = roadrunner.RoadRunner()

currentModel = ''


@app.task
def add(x, y):
    return x + y


@app.task
def rrRun(method, *params):
    if (method is not None):
        if (method == 'load'):
            # Override load method
            newModel = md5.new(*params).digest()
            global currentModel
            if (newModel == currentModel):
                # Model already loaded
                pass
            else:
                currentModel = newModel
                rr.load(*params)
        elif (isinstance(method, basestring)):
            return getattr(rr, method)(*params)
        else:
            fun = getattr(rr, method.pop(0))
            for m in method:
                fun = getattr(fun, m)
            return fun(*params)


@app.task
def rrChain(commands):
    results = []
    for command in commands:
        results.append(rrRun(*command))
    return results
