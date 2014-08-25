from __future__ import unicode_literals

from ..interface import BrokerInterface


class DatabaseMessageBroker(BrokerInterface):

    def produce_message(self, data):
        pass

    def consume_message(self, handler):
        pass

    def keep_consuming(self, handler):
        pass