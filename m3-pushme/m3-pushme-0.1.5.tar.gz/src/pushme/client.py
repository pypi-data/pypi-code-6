# -*- coding: utf-8 -*-
"""
CLI-программа, демонстрирующая API отправки сообщений
"""
import mq, options


if __name__ == '__main__':
    config = options.configure(
        "Simple Client for PushMe",
        options=(
            options.MQ_OPTIONS
        ) + (
            {
                'switches': ("-i", "--id"),
                'dest': "uid",
                'type': "int",
                'help': "target UID",
                'default': None,
            },
            {
                'switches': ("-t", "--topic"),
                'dest': "topic",
                'help': "topic",
                'default': None,
            }
        ),
        queue_backend="snakemq",
        queue_host="localhost",
        queue_port=4000
    )
    client = mq.get_sender(
        config.queue_backend,
        (config.queue_host, config.queue_port)
    )
    print "Messages will be sent to %s..." % (
        'UID=%d' % config.uid
        if config.uid else
        'all connected users'
    )
    while True:
        text = raw_input('message:')
        if text:
            client.send(text, config.uid, config.topic)
