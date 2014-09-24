# -*- coding: utf-8 -*-
"""
Базовые классы для queue backends
"""
import abc


class Queue(object):
    """
    Сервер очереди
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, addr, quiet=False):
        """
        :addr - (host, port), на котором сервер создаст сокет
        """
        self._addr = addr
        self._quiet = quiet

    @abc.abstractmethod
    def run(self):
        pass


class _Client(object):
    """
    Абстракстный клиент
    """

    def __init__(self, ident, queue_addr, quiet=False):
        """
        :ident      - идентификатор отправителя
        :queue_addr - (host, port) сервера очереди
        """
        self._ident = ident
        self._queue_addr = queue_addr
        self._quiet = quiet


class Sender(_Client):
    """
    Клиент-отправитель
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, data, uid=None, topic=None):
        """
        Отправляет сообщение получателю посредством очереди
        :uid :: int - id socket-соединения
        :topic - тема сообщения
        :data - данные для отправки
        """
        pass


class Receiver(_Client):
    """
    Клиент-получатель
    """
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def _default_callback(uid, topic, data):
        """
        Умолчательный обработчик получения сообщений
        """
        pass

    # атрибут, хранящий функцию - обработчик получения сообщений
    callback = _default_callback

    @abc.abstractmethod
    def process(self):
        """
        Производит получение сообщений
        (это callback для асинхронного ядра tornado)
        """
        pass
