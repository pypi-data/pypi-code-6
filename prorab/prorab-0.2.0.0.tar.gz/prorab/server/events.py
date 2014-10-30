from prorab.server import send_all
from prorab import log


def task_pulled(message):
    log.log('[QUEUE] Command {} pulled from queue', message)


@send_all
def task_started(c, m):
    log.log('[EXEC] Started executing command {}', m)
    c.sendJson({'type': 'event',
        'event': 'task-started',
        'name': m, })


@send_all
def task_finished(c, p):
    log.log('[EXEC] Executing finished, returned code {}', p)
    c.sendJson({'type': 'event',
        'event': 'task-finished',
        'code': p, })


@send_all
def task_not_found(c, name):
    log.error('[EXEC] Task {} not found on local commands database!', name)
    c.sendJson({'type': 'error',
        'message': 'task {} notfound'.format(name), })


@send_all
def task_failed(c, exception):
    log.error('[EXEC] Task execution failed with exception "{}"', exception)
    c.sendJson({'type': 'error',
        'message': 'exception while running task: ' + exception, })

@send_all
def task_interrupted(c, signal, user):
    log.error('[EXEC] Task interrupted by signal {} by user {}', signal, user)
    c.sendJson({'type': 'event',
            'event': 'task-interrupted',
            'signal': signal, })
