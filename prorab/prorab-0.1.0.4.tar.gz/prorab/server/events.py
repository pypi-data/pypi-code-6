from prorab.server import send_all


def task_pulled(message):
    pass


@send_all
def task_started(c, m):
    c.sendJson({'type': 'event',
        'event': 'task-started',
        'name': m, })


@send_all
def task_finished(c, p):
    c.sendJson({'type': 'event',
        'event': 'task-finished',
        'code': p, })


@send_all
def task_not_found(c, name):
    c.sendJson({'type': 'error',
        'message': 'task {} notfound'.format(name), })


@send_all
def task_failed(c, exception):
    c.sendJson({'type': 'error',
        'message': 'exception while running task: ' + exception, })
