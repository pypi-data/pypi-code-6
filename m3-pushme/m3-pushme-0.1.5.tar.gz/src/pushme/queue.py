# -*- coding: utf-8 -*-
"""
Сервер очереди сообщений на отправку
"""
import mq
import options

__VERSION__ = "0.1"

PROG_NAME = 'PushMe MQ Server v.%s' % __VERSION__


if __name__ == '__main__':
    # парсинг опций ком.строки
    config = options.configure(
        PROG_NAME,
        options=(
            options.HOST,
            options.PORT,
            options.QUEUE_BACKEND,
            options.QUIET
        ),
        host="", port=4000,
        queue_backend='snakemq'
    )
    # запуск сервера очереди
    mq.get_queue(
        backend=config.queue_backend,
        addr=(config.host, config.port),
        quiet=config.quiet
    ).run()
