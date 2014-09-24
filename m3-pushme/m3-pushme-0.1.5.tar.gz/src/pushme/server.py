# -*- coding: utf-8 -*-

import json

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

from pushme import mq, options


__VERSION__ = "0.1"

PROG_NAME = 'PushMe Socket Server v.%s' % __VERSION__

UID_POOL = {}

QUEUE_PROCCESSING_TIMEOUT = 50 # ms


class PushConnection(SockJSConnection):
    """
    SockJS-соединение для отправки сообщений в браузер
    """
    _uid = None

    def on_open(self, request):
        self._uid = None

    def on_close(self):
        conns = UID_POOL[self._uid]
        conns.remove(self)
        if not conns:
            UID_POOL.pop(self._uid)

    def on_message(self, msg):
        if not self._uid:
            try:
                self._uid = int(msg)
            except TypeError:
                # клиент не должен слать ничего, кроме uid
                pass
            else:
                UID_POOL.setdefault(self._uid, set()).add(self)
                self.send('{"topic": "system", "data": "registered"}')


def receive_callback(uid, topic, data):
    """
    callback, обрабатывающий сообщения из очереди
    """
    if uid == 0:
        # широковещательное сообщение
        targets = UID_POOL.values()
    else:
        try:
            targets = [UID_POOL[uid]]
        except KeyError:
            # сообщения, адресованные uid'у, который не зарегистрирован
            # в этом экземпляре сервера, игнорируются
            return

    msg = {'data': data}
    if topic is not None:
        msg['topic'] = topic
    msg = json.dumps(msg)

    for target_set in targets:
        for t in target_set:
            t.send(msg)


if __name__ == '__main__':
    # разбор опций
    config = options.configure(
        PROG_NAME,
        options=options.ALL_OPTIONS,
        host="localhost", port=9999,
        queue_host="localhost",
        queue_port=4000,
        queue_backend="snakemq"
    )

    # получатель сообщений из очереди
    receiver = mq.get_receiver(
        backend=config.queue_backend,
        queue_addr=(config.queue_host, config.queue_port),
        quiet=config.quiet
    )
    receiver.callback = receive_callback

    # роутер/сервер сокетов
    router = SockJSRouter(PushConnection, '/pull', {'verify_ip': False})
    app = web.Application(router.urls)
    app.listen(config.port)

    # встраивание поучателя сообщений из очереди в основной цикл Tornado
    loop = ioloop.IOLoop.instance()
    pc = ioloop.PeriodicCallback(
        receiver.process, QUEUE_PROCCESSING_TIMEOUT, loop)
    pc.start()

    # запуск основного цикла Tornado
    if not config.quiet:
        print "%s started at %s:%s" % (PROG_NAME, config.host, config.port)
    loop.start()
