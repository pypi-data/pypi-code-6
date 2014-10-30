from boto import sqs

from twisted.internet import task

from prorab import command, server, config, log
from prorab.server import events

import threading
import sys
import hashlib
import json


def start():
    for override in sys.argv[1:]:
        k, v = override.split('=')
        default = getattr(config, k)
        if type(default) is int:
            v = int(v)
        elif type(default) is list:
            v = v.split(',')

        setattr(config, k, v)

    log.log('Daemon starting')

    conn = sqs.connect_to_region(
        config.region,
        aws_access_key_id=config.id,
        aws_secret_access_key=config.key,
    )

    general_queue = conn.get_queue(config.general_queue)
    personal_queue = conn.get_queue(config.personal_queue)

    def pull_queue():
        if not command.is_working():
            for queue in [personal_queue, general_queue, ]:
                message = queue.read()
                if message:
                    queue.delete_message(message)
                    events.task_pulled(message.get_body())
                    command.execute(message.get_body())
                    return

    task.LoopingCall(command.send_out).start(config.SEND_OUT)
    task.LoopingCall(pull_queue).start(config.PULL_QUEUE)
    task.LoopingCall(server.ping).start(config.PING)

    flag = threading.Event()
    threading.Thread(target=command.io_thread, args=(flag, )).start()

    def check_hash(c, m):
        hash = ''.join([a + b for a, b in config.commands.items()])
        if hashlib.md5(hash).hexdigest() != m:
            return {'type': 'error',
                    'message': 'command hash check failed', }
        else:
            return {'type': 'event',
                    'event': 'command-hash-checked', }

    server.register_command('commands_hash', check_hash)

    log.log('Daemon started')
    server.start()
    flag.set()
