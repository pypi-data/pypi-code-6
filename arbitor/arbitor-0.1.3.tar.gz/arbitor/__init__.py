# -*- coding: utf-8 -*-

import os
import time
import logging
import thread
import etcd

logger = logging.getLogger(__name__)


class Arbitor(object):
    def __init__(self, etcd_uri, callback, read_timeout=9):
        self.callback = callback
        self.etcd_client = etcd.Client(etcd_uri)
        self.etcd_read_timeout = read_timeout

    def pool_config(self, key):
        new_config = False

        while not new_config:
            begin = time.time()
            try:
                new_config = self.etcd_client.watch(
                    key, timeout=self.etcd_read_timeout)
            except etcd.EtcdException:
                if time.time() - begin < 30:
                    time.sleep(30)

        return new_config

    def pre_watch(self):
        pass

    def do_callback(self, config):
        self.callback(config)

    def do_watch(self, key):
        while True:
            try:
                config = self.pool_config(key)
                if config:
                    self.do_callback(config)
            except Exception:
                logger.exception("failed to fetch config")

    def watch(self, key):
        self.pre_watch()
        self.do_watch(key)


class ForkArbitor(Arbitor):
    def __init__(self, *args, **kwds):
        super(ForkArbitor, self).__init__(*args, **kwds)

    def pre_watch(self):
        self.master_pid = os.getpid()

        if os.fork() != 0:
            return

    def do_callback(self, config):
        return self.callback(self.master_pid, config)


class ThreadingArbitor(Arbitor):
    def watch(self, key):
        thread.start_new_thread(super(ThreadingArbitor, self).watch, (key, ))


def install_etcd_watcher(etcd_uri, callback):
    return Arbitor(callback).watch()
