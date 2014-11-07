#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""Internal write plugin which log all values and
events using ``DEBUG`` severity.
"""

from drove.plugin import Plugin


class LogPlugin(Plugin):
    def write(self, channel):
        for data in channel.receive("droveio.log"):
            self.log.debug(str(data))
