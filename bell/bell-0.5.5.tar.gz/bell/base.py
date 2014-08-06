# coding=utf8

"""
bell.base
~~~~~~~~~

The based service class.
"""

from logging.handlers import RotatingFileHandler

import beanstalkc
from ssdb import SSDBClient

from bell.configs import configs
from bell.logger import formatter, level_mappings, logger


def serve_wrapper(func):
    def _func(service, *args, **kwargs):
        if service.debug:
            return func(service, *args, **kwargs)
        try:
            return func(service, *args, **kwargs)
        except KeyboardInterrupt:
            service.shutdown()
    return _func


class Service(object):
    """
    Interfaces should be implemented:

        service.serve()
        service.shutdown()
        service.name
    """

    name = None

    def __init__(self):
        self.debug = False

    def initialize_logger(self):
        logger.name = 'bell.{0}'.format(self.name)
        enable = configs[self.name]['log']['path']
        path = configs[self.name]['log']['path']
        max_bytes = configs[self.name]['log']['maxBytes']
        backup_count = configs[self.name]['log']['backupCount']
        logging_level = configs[self.name]['log']['level']

        if enable:
            fh = RotatingFileHandler(path, maxBytes=max_bytes,
                                     backupCount=backup_count)
            fh.setFormatter(formatter)
            fh.setLevel(level_mappings[logging_level])
            logger.addHandler(fh)

    def initialize_ssdb(self):
        host = configs['ssdb']['host']
        port = configs['ssdb']['port']
        return SSDBClient(host=host, port=port)

    def initialize_beans(self, as_watcher=False, as_user=False):
        host = configs['beanstalkd']['host']
        port = configs['beanstalkd']['port']
        tube = configs['beanstalkd']['tube']
        beans = beanstalkc.Connection(
            host=host, port=port, parse_yaml=False)
        if as_watcher:
            beans.watch(tube)
        if as_user:
            beans.use(tube)
        return beans

    def shutdown(self):
        pass

    def serve(self):
        pass
