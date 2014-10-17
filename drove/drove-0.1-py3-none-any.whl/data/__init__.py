#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The data module contains definitions of data used in drove
client-server communication
"""

from ..importer import Importer


class Data(object):
    @classmethod
    def from_dump(cls, dump_str):
        """Create a Data from a dump representation"""
        if dump_str.startswith("V|"):
            fields = dump_str.split("|", 6)
            if len(fields) < 6:
                raise ValueError("The Value has missing fields")
            kls = Importer("drove.data")
            timestamp, nodename, plugin, value, vtype = fields[1:]
            return kls("value", plugin, value, nodename, vtype, timestamp)
        elif dump_str.startswith("E|"):
            fields = dump_str.split("|", 6)
            if len(fields) < 6:
                raise ValueError("The Event has missing fields")
            kls = Importer("drove.data")
            timestamp, nodename, plugin, severity, message = fields[1:]
            return kls("event", plugin, severity, message, nodename, timestamp)
        else:
            raise ValueError("Unable to get data from dump")

    def is_value(self):
        return self.__class__.__name__ == 'Value'

    def is_event(self):
        return self.__class__.__name__ == 'Event'
