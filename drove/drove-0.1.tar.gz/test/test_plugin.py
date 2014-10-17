#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from drove.config import Config
from drove.channel import Channel
from nose.tools import raises

import drove.plugin


class TestingPlugin(drove.plugin.Plugin):
    def read(self):
        self.emit(None)

    def write(self, channel):
        assert channel.__class__.__name__ == "Channel"

    def start(self):
        pass


class TestingFailedPlugin(drove.plugin.Plugin):
    importer_name = "testing"
    count = 0

    def read(self):
        raise Exception

    def write(self, channel):
        raise Exception

    def _mock_log(self, *args, **kwargs):
        if self.count == 1:
            raise AssertionError
        else:
            self.count = 1


class TestingStartPlugin(drove.plugin.Plugin):
    importer_name = "testing"
    value = []

    def read(self):
        self.value.append("read")

    def write(self, channel):
        self.value.append("write")


def test_plugin_load():
    """Testing Plugin: load()"""
    config = Config()
    path = os.path.join(os.path.dirname(__file__), "plugin")
    config["plugin_dir"] = path
    channel = Channel()
    channel.subscribe("test")
    x = drove.plugin.Plugin.load("cpu", config, channel)
    assert x.__class__.__name__ == "CpuPlugin"


def test_plugin_rw():
    """Testing Plugin: read() and write()"""
    config = Config()
    channel = Channel()
    channel.subscribe("test")

    x = TestingPlugin(config, channel)
    x.setup(config)
    x._read()
    x._write()


@raises(AssertionError)
def test_plugin_start():
    """Testing Plugin: start() with handlers"""

    config = Config()
    channel = Channel()
    config["read_interval"] = 0
    config["write_interval"] = 0
    channel.subscribe("test")

    x = TestingStartPlugin(config, channel)
    x.start()
    assert "read" in x.value
    assert "write" in x.value


def test_plugin_manager_loop():
    """Testing PluginManager: waiting loop"""
    config = Config()
    channel = Channel()
    x = drove.plugin.PluginManager(config, channel)
    x.loop(1000, 0)


def test_plugin_manager():
    """Testing PluginManager: basic behaviour"""

    config = Config()
    channel = Channel()
    config["read_interval"] = 0
    config["write_interval"] = 0
    path = os.path.join(os.path.dirname(__file__), "plugin")
    config["plugin_dir"] = path
    config["plugin.cpu"] = True
    channel.subscribe("test")

    x = drove.plugin.PluginManager(config, channel)
    assert x.plugins[0].__class__.__name__ == "CpuPlugin"
    x.plugins = [TestingPlugin(config, channel)]
    x.start_all()
    assert len(x) == 1
    assert len([i for i in x]) == 1
    x.stop_all()


@raises(AssertionError)
def test_plugin_rw_ex():
    """Testing Plugin: read() and write() exception"""

    config = Config()
    channel = Channel()
    channel.subscribe("test")

    x = TestingFailedPlugin(config, channel)
    x.log.error = x._mock_log
    x._read()
    x._write()
