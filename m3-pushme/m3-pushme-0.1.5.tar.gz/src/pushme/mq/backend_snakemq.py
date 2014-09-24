# -*- coding: utf-8 -*-
"""
Очередь на базе snakeMQ.
Подходит для использования на машинах разработчиков,
т.к. является pure-python.
"""

from pushme.mq import interface
from snakemq import messaging, message, link, packeter


class Queue(interface.Queue):
    """
    Простой сервер очереди на ОДНОГО получателя и несколько отправителей
    """

    def __init__(self, *args, **kwargs):
        super(Queue, self).__init__(*args, **kwargs)
        self._link = link.Link()
        self._link.add_listener(self._addr)
        self._packeter = packeter.Packeter(self._link)
        self._messaging = messaging.Messaging(
            "queue", "", self._packeter)
        self._packeter.on_connect.add(self._handle_connect)
        self._packeter.on_disconnect.add(self._handle_disconnect)
        self._messaging.on_message_recv.add(self._broadcast)

    def _handle_connect(self, conn_id):
        if not self._quiet:
            print "Connected: ", conn_id

    def _handle_disconnect(self, conn_id):
        if not self._quiet:
            print "Disconnected: ", conn_id

    def _broadcast(self, conn, sender, msg):
        self._messaging.send_message(
            "receiver", msg)

    def run(self):
        if not self._quiet:
            print "snakeMQ started at %s:%s" % (
                self._addr[0] or "localhost",
                self._addr[1]
            )
        self._link.loop()


def _configure_client(obj):
    """
    Конфигурирует клиент snakeMQ
    """
    obj._link = link.Link()
    obj._link.add_connector(obj._queue_addr)
    obj._packeter = packeter.Packeter(obj._link)
    obj._messaging = messaging.Messaging(obj._ident, "", obj._packeter)


class Sender(interface.Sender):
    """
    Простой отправитель.
    """
    msg_ttl = 500
    loop_timeout = 0.02
    loop_len = 2

    def __init__(self, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)
        _configure_client(self)

    def send(self, data, uid=None, topic=None):
        """
        Отправляет сообщение получателю посредством очереди
        :uid :: int - id socket-соединения
        :topic - тема сообщения
        :data - данные для отправки
        """
        self._messaging.send_message(
            "queue",
            message.Message(
                bytes(
                    '%s|%s|%s' % (
                        uid or 0,
                        topic or "",
                        data.encode('utf-8')
                    )),
                ttl=self.msg_ttl
            ))
        self._link.loop(runtime=self.loop_timeout, count=self.loop_len)


class Receiver(interface.Receiver):
    """
    Простой получатель.
    В данной реализации очереди может быть ТОЛЬКО ОДИН получатель!
    """
    loop_timeout = 0.1

    def __init__(self, *args, **kwargs):
        super(Receiver, self).__init__(*args, **kwargs)
        _configure_client(self)
        self._messaging.on_message_recv.add(self._on_recv)

    def _on_recv(self, conn, sender, msg):
        try:
            uid, topic, data = str(msg.data).split('|', 2)
            topic = topic.strip() or None
            uid = int(uid)
        except (ValueError, TypeError):
            print "Wrong message format:", msg.data
        else:
            self.callback(uid, topic, data)

    def process(self):
        self._link.loop(runtime=self.loop_timeout)
