# -*- coding: utf-8 -*-
"""
Подсистема наcтройки компонент через ком.строку
"""

import optparse
import sys

PORT = {
    'switches': ("-p", "--port"),
    'dest': "port",
    'type': "int",
    'help': "port"
}

HOST = {
    'switches': ("-H", "--host"),
    'dest': "host",
    'type': "str",
    'help': "host"
}

QUIET = {
    'switches': ("-q", "--quiet"),
    'dest': "quiet",
    'action': "store_true",
    'default': False,
    'help': "be quiet"
}

QUEUE_HOST = {
    'switches': ("-m", "--mq-host"),
    'dest': "queue_host",
    'type': "str",
    'default': "localhost",
    'help': "message queue host"
}

QUEUE_PORT = {
    'switches': ("-P", "--mq-port"),
    'dest': "queue_port",
    'type': "int",
    'help': "message queue port"
}

QUEUE_BACKEND = {
    'switches': ("-B", "--mq-backend"),
    'dest': "queue_backend",
    'type': "str",
    'help': "message queue backend name"
}

LISTENER_OPTIONS = (HOST, PORT)
MQ_OPTIONS = (QUEUE_BACKEND, QUEUE_HOST, QUEUE_PORT)
ALL_OPTIONS = (QUIET,) + LISTENER_OPTIONS + MQ_OPTIONS


def configure(prog, options, **defaults):
    """
    Возвращает парсер ключей ком.строки для компоненты
    """
    option_list = []
    for o in options:
        o = o.copy()
        try:
            o['default'] = defaults[o['dest']]
        except KeyError:
            pass
        option_list.append(
            optparse.make_option(*o.pop('switches'), **o))

    parser = optparse.OptionParser(
        option_list=option_list, prog=prog)

    config, unparsed = parser.parse_args()
    if unparsed:
        print "Unknown arg(s)!:\n" + "\n".join(unparsed)
        parser.print_help()
        sys.exit(1)
    return config
