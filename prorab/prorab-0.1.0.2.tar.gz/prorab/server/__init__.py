from twisted.internet.protocol import Factory
from prorab.server.helpers import JSONReceiver
from twisted.internet import reactor
from txsockjs.factory import SockJSFactory

import time

from prorab import config


stdout_subs = []
clients = []
commands = {}


def send_all(f):
    def wrap(*args, **kwargs):
        for c in clients:
            f(c, *args, **kwargs)
    return wrap


def call(name, *args, **kwargs):
    if name in commands:
        return commands[name](*args, **kwargs)
    else:
        raise RuntimeError('no such command')


def register_command(name, ifn):
    commands[name] = ifn


class ProrabProtocol(JSONReceiver):
    stdout_start = None

    def connectionMade(self):
        pass

    def connectionLost(self, s):
        try:
            clients.remove(self)
        except ValueError:
            pass
        self.unsubscribe()

    def unsubscribe(self):
        try:
            stdout_subs.remove(self)
            return {'type': 'event',
                    'event': 'unsubscribed', }
        except ValueError:
            pass

    def subscribe(self):
        stdout_subs.append(self)
        return {'type': 'event',
                'event': 'subscribed', }

    def jsonReceived(self, data):
        cmd = data.get('command')
        args = data.get('args', [])

        if cmd == 'auth':
            token = args[0] if len(args) > 0 else None
            if token == config.ACCESS_TOKEN:
                clients.append(self)
                self.sendJson({'type': 'event',
                    'event': 'authorized', })
                return
            else:
                self.sendJson({'type': 'error',
                    'message': 'wrong token', })
                return

        if self not in clients:
            self.sendJson({'type': 'error',
                    'message': 'not authorized', })
        else:
            try:
                self.sendJson(call(cmd, self, *args))
            except RuntimeError as e:
                self.sendJson({'type': 'error',
                        'message': str(e), })


@send_all
def send_task_started(c, m):
    c.sendJson({'type': 'event',
        'event': 'task-started',
        'name': m, })


@send_all
def send_task_finished(c, p):
    c.sendJson({'type': 'event',
        'event': 'task-finished',
        'code': p, })


@send_all
def ping(c):
    c.sendJson({'type': 'ping', })


def start():
    print('Starting server at {}'.format(config.WEBSOCKET_PORT))
    reactor.listenTCP(config.WEBSOCKET_PORT, SockJSFactory(Factory.forProtocol(ProrabProtocol)))
    reactor.run()


register_command('stdout_sub', lambda x: x.subscribe())
register_command('stdout_unsub', lambda x: x.unsubscribe())
register_command('ping', lambda x: {'type': 'ping', 'time': time.time()})
