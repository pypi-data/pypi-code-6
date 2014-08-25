from __future__ import unicode_literals


class BrokerInterface(object):

    def __init__(self):
        self.prepare()

    def prepare(self):
        pass

    def produce_message(self, *args, **kwargs):
        raise NotImplementedError()

    def consume_message(self, handler):
        raise NotImplementedError()

    def consume_messages(self, handler):
        raise NotImplementedError()