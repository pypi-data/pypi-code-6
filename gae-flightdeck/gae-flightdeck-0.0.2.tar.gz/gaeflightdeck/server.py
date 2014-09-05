#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()
monkey.patch_sys(stdin=True, stdout=False, stderr=False)
import gevent
from gevent.queue import Queue
import signal
import sys
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from .formatter import process_log
from .web_server import make_server

q = Queue()


def producer():
    while True:
        line = sys.stdin.readline()
        process_log(line, q.put)


class LogNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def sendlogs():
            while True:
                while not q.empty():
                    val = q.get(True)
                    self.emit('log', {'line': val})
                gevent.sleep(1)

        self.spawn(sendlogs)


def main():
    gevent.signal(signal.SIGQUIT, gevent.kill)

    server = make_server({
        '/logs': LogNamespace
    })

    greenlets = [
        gevent.spawn(producer)
    ]

    try:
        server.start()
        print 'Log webserver running on http://127.0.0.1:51324'
        gevent.joinall(greenlets)
    except KeyboardInterrupt:
        print "Exiting..."


if __name__ == '__main__':
    main()
