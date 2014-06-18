#-*- coding: utf-8 -*-

from middleware import *

class LogConsole:

    def __init__(self, amqp_config, output=sys.stdout):
        self.conf = amqp_config
        self.output = output

    def run(self):
        consumer = AMQP_LogConsumer(self.conf)
        consumer.open()
        consumer.setOutput(self.output)
        consumer.consume_forever()
        consumer.close()
