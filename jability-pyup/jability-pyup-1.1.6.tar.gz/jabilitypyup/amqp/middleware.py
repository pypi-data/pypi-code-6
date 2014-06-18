#-*- coding: utf-8 -*-

from amqplib import client_0_8 as amqp
import logging
import json
import os
import time
import sys

class AMQP_Connection:

    def __init__(self, amqp_config):
        """Exemple de conf. attendue
        {
                    'exchange': {
                                'name': 'notify.user.sync',
                                'type': 'fanout',
                                'durable': True,
                                'auto_delete': False,
                                'delivery_mode': 2
                                },
                    'queue': {
                                'name': [ 'notify.user.sync.test', ],
                                'durable': True,
                                'auto_delete': False,
                                'exclusive': False
                                },
                    'host': {
                                'name': 'srvdev',
                                'user': 'accreq',
                                'password': 'password',
                                'virtual_host': '/ijg/dev',
                                'insist': False
                                },
                    'consumer': {
                                'queue': 'notify.user.sync.test',
                                'no_ack': False,
                                'nowait': True,
                                'tag': 'consumer.test'
                                }
        """
        self.cfg = amqp_config

    def open(self):
        try:
            self.conn = amqp.Connection( host=self.cfg['host']['name'],
                            userid=self.cfg['host']['user'],
                            password=self.cfg['host']['password'],
                            virtual_host=self.cfg['host']['virtual_host'],
                            insist=self.cfg['host']['insist'])
            self.chan = self.conn.channel()
            self.chan.exchange_declare(  exchange = self.cfg['exchange']['name'],
                            type = self.cfg['exchange']['type'],
                            durable = self.cfg['exchange']['durable'],
                            auto_delete = self.cfg['exchange']['auto_delete'])
            for qname in self.cfg['queue']['name']:
                self.chan.queue_declare(  qname,
                                    durable = self.cfg['queue']['durable'],
                                    auto_delete = self.cfg['queue']['auto_delete'],
                                    exclusive = self.cfg['queue']['exclusive'])
                self.chan.queue_bind(   queue = qname,
                                        exchange=self.cfg['exchange']['name'] )
        except Exception as e:
            logging.error(u'AMQP_Connection : Error during open() : %s' % (e))
        logging.debug(u"AMQP_Connection : open exchange '%s'" % (self.cfg['exchange']['name']))

    def close(self):
        try:
            self.chan.close()
            self.conn.close()
        except Exception as e:
            logging.error(u'AMQP_Connection : Error during close() : %s' % (e))
        logging.debug(u"AMQP_Connection : close exchange '%s'" % (self.cfg['exchange']['name']))


class AMQP_Publisher(AMQP_Connection):

    def __init__(self, amqp_config):
        AMQP_Connection.__init__(self, amqp_config)

    def send_message(self, message):
        try:
            msg = amqp.Message(message)
            msg.properties["delivery_mode"] = self.cfg['exchange']['delivery_mode']
            self.chan.basic_publish( msg,
                                exchange = self.cfg['exchange']['name'])
        except Exception as e:
            logging.error(u'AMQP_Publisher : Error during send_message() : %s' % (e))
        logging.debug(u"AMQP_Publisher : send message on exchange '%s'" % (self.cfg['exchange']['name']))

    def open_send_and_close(self, message):
        self.open()
        self.send_message(message)
        self.close()


class AMQP_Consumer(AMQP_Connection):

    def __init__(self, amqp_config, callback_function=None):
        AMQP_Connection.__init__(self, amqp_config)
        self.callback_function = callback_function

    def callback(self, msg):
        if(self.callback_function):
            self.callback_function(msg)
        else:
            logging.error(u'AMQP_Consumer : message receive but no call back declared !')

    def consume_forever(self):
        self.chan.basic_consume(    self.cfg['consumer']['queue'],
                                    callback=self.callback,
                                    no_ack=self.cfg['consumer']['no_ack'],
                                    nowait=self.cfg['consumer']['nowait'],
                                    consumer_tag=self.cfg['consumer']['tag'])
        while self.chan.callbacks:
            try:
                self.chan.wait()
            except KeyboardInterrupt as e:
                break

class AMQP_LogHandler(logging.Handler):

    def __init__(self, amqp_publisher):
        self.broadcaster = amqp_publisher
        self.level = 0
        self.filters = []
        self.lock = 0
        self.machine = os.uname()[1]
        self.broadcaster.open()

    def emit(self, record):
        message = { "name": record.name,
                    "machine": self.machine,
                    "message": record.msg % record.args,
                    "levelname": record.levelname,
                    "levelno": record.levelno,
                    "pathname": record.pathname,
                    "lineno": record.lineno,
                    "exception": record.exc_info,
                    "asctime": record.created,
                    "fdate": time.strftime('%Y%m%d', time.localtime(record.created)),
                    "ftime": time.strftime('%H%M%S', time.localtime(record.created)),
                    "timezone": time.strftime('%Z', time.localtime(record.created)),
                    "process": record.process,
                    "thread": record.thread,
                    "threadName": record.threadName,
                    "funcName": record.funcName,
                    "module": record.module,
                    "filename": record.filename,
                    }
        json_msg = json.dumps(message)
        self.broadcaster.send_message( json_msg )

    def close(self):
        self.broadcaster.close()

    @staticmethod
    def getStreamAndBroadcastLogHandler(
                                namespace,
                                amqp_config,
                                level=logging.DEBUG):
        "Factory function for a logging.StreamHandler instance connected to your namespace."

        logging.basicConfig(    datefmt='%Y%m%d %H%M%S',
                                format="%(asctime)s - %(levelname)s - %(name)s - %(filename)s %(funcName)s %(lineno)d - %(message)s")

        logger = logging.getLogger(namespace)
        logger.setLevel(level)

        amqp_producer = AMQP_Publisher(amqp_config)
        handler_messages = AMQP_LogHandler(amqp_producer)
        logger.addHandler(handler_messages)

        return logger


class AMQP_LogConsumer(AMQP_Consumer):

    DEFAULT_FORMAT = "%(fdate)s %(ftime)s - %(levelname)s - %(machine)s - %(name)s - %(filename)s %(funcName)s %(lineno)d - %(message)s"

    def __init__(self, amqp_config, callback=None):
        AMQP_Consumer.__init__(self, amqp_config, self.callback)
        self.logcallback = callback
        self.setFormat()
        self.setOutput()

    def setFormat(self, format=None):
        if format == None:
            self.format = AMQP_LogConsumer.DEFAULT_FORMAT
        else:
            self.format = format

    def setOutput(self, stream=sys.stdout):
        self.stream = stream

    def callback(self, msg):
        message = json.loads(msg.body)
        msg.channel.basic_ack(msg.delivery_tag)
        print >>self.stream, self.msg2str(message)
        if not self.logcallback==None:
            self.logcallback(msg)

    def msg2str(self, message):
        return self.format % message


if __name__ == '__main__':
    amqp_config = {
                    'exchange': {
                                'name': 'notify.log.add',
                                'type': 'fanout',
                                'durable': True,
                                'auto_delete': False,
                                'delivery_mode': 2
                                },
                    #'queue': {
                    #            'name': [   'notify.log.add.console', ],
                    #            'durable': True,
                    #            'auto_delete': True,
                    #            'exclusive': False
                    #            },
                    'host': {
                                'name': 'srvdev',
                                'user': 'accreq',
                                'password': 'accreq',
                                'virtual_host': '/ijg/dev',
                                'insist': False
                                },
                    'consumer': {
                                'queue': None,
                                'no_ack': False
                                }
                    }

    logger = AMQP_LogHandler.getStreamAndBroadcastLogHandler("your-namespace", amqp_config, logging.INFO)
    logger.info("yo baby")
    logger.error("o noes")

