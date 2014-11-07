#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
from drove.config import Config
from drove.channel import Channel
from drove.data.value import Value

from . import log


class TestLogPlugin(unittest.TestCase):
    def test_log_plugin(self):
        config = Config()
        channel = Channel()
        channel.subscribe("droveio.log")
        channel.publish(Value("test", 0))

        kls = log.LogPlugin(config, channel)
        kls.plugin_name = "droveio.log"
        kls.write(channel)
