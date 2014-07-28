#!/usr/bin/env python
# encoding: utf-8

import logging
logger = logging.getLogger('async')

import asyncore
from smtpd import DebuggingServer

class Server(DebuggingServer):

    def process_message(self, peer, mail, rcpttos, data):
        logger.debug(peer)

f = Server(('0.0.0.0', 25001), '0.0.0.0')

try:
    asyncore.loop()
except KeyboardInterrupt:
    pass
