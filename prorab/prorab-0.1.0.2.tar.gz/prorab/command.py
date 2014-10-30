import time
import subprocess
import signal

from prorab.server import events
from prorab import server
from prorab import config

execution_poll = []
stdout_poll = []
pull_poll = []
stdout_buffer = []


def get_process():
    if execution_poll:
        return execution_poll[0]


def pop_process():
    del execution_poll[0]


def is_working():
    return get_process()


def popen(args):
    p = subprocess.Popen(args, cwd=config.dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p


def execute(name, args=None):
    line = config.commands.get(name)
    if not line:
        events.task_not_found(name)
        return

    events.task_started(name)

    for c in server.stdout_subs:
        c.stdout_start = 0

    while True:
        try:
            del pull_poll[0]
            del stdout_buffer[0]
        except IndexError:
            break

    while True:
        try:
            del stdout_buffer[0]
        except IndexError:
            break

    print('Executing {}'.format(line))
    p = popen(line.split())
    execution_poll.append(p)
    stdout_poll.append(p.stdout)


def send_out():
    for c in server.stdout_subs:
        if c.stdout_start == None:
            c.stdout_start = len(stdout_buffer)

        payload = stdout_buffer[c.stdout_start:]
        if payload:
            c.stdout_start += len(payload)
            c.sendJson({'type': 'stdout', 'payload': ''.join(payload), })


def io_thread(flag):
    while not flag.is_set():
        p = get_process()
        if not p:
            time.sleep(config.IO_THREAD)
            continue

        out = p.stdout
        contents = out.read(config.STDOUT_BUFFER_LENGTH)
        stdout_buffer.append(contents)

        if len(contents) < config.STDOUT_BUFFER_LENGTH:
            stdout_buffer.append('prorab: command finished with {}\n'.format(p.poll()))
            events.task_finished(p.poll())
            pop_process()
            print('Process finished')


def sig_int():
    p = get_process()
    if p:
        print('Interrupted by terminal')
        p.send_signal(signal.SIGINT)
        return {'type': 'event',
                'event': 'task-interrupted', }
    return {'type': 'error',
            'message': 'no active task', }


def sig_kill():
    p = get_process()
    if p:
        print('Terminated by terminal')
        p.terminate()
        return {'type': 'event',
                'event': 'task-terminated', }
    return {'type': 'error',
            'message': 'no active task', }

server.register_command('status', lambda x: {'type': 'status', 'status': 'working' if get_process() else 'idle'})
server.register_command('sigint', lambda x: sig_int())
server.register_command('sigterm', lambda x: sig_kill())
