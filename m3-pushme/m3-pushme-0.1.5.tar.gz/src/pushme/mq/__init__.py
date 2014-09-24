# -*- coding: utf-8 -*-
"""
Очередь сообщений.
Предоставляет единый интерфейс для различных реализаций очередей.
"""
from uuid import uuid4
import importlib


def _import_thing(module, thing):
    try:
        m = importlib.import_module('pushme.mq.backend_%s' % module)
    except ImportError:
        raise
        raise RuntimeError(u'Unknown MQ backend: %r' % module)
    try:
        return getattr(m, thing)
    except AttributeError:
        raise RuntimeError(u'Bad MQ backend: %r' % module)


def get_queue(backend, *args, **kwargs):
    """
    Возвращает реализацию сервера очереди
    :backend - имя конкретной реализации очереди
    """
    return _import_thing(backend, 'Queue')(*args, **kwargs)


def get_sender(backend, *args, **kwargs):
    """
    Возвращает реализацию клиента - отправителя сообщений
    :backend - имя конкретной реализации очереди
    """
    return _import_thing(
        backend, 'Sender'
    )(
        str(uuid4()), *args, **kwargs
    )


def get_receiver(backend, *args, **kwargs):
    """
    Возвращает реализацию клиента - получателя сообщений
    :backend - имя конкретной реализации очереди
    """
    return _import_thing(
        backend, 'Receiver'
    )(
        # все получатели имеют имя "receiver"
        'receiver', *args, **kwargs
    )
