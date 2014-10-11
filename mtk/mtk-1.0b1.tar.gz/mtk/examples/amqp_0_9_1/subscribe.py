#!/usr/bin/env python

import optparse
import os
import signal
import ssl
import sys
import time

from mtk.amqp_0_9_1 import *

from publish import connect,parser

#######################################################################################################################

keep_running = True

def sigHandler(signal, frame):
    global keep_running
    keep_running = False

signal.signal(signal.SIGINT, sigHandler)
            
#######################################################################################################################

def subscribe(channel, exchange, filter):
    print("subscribing to exchange %s for messages matching '%s'" % (exchange,filter))
    queue = channel.queueDeclare()
    channel.queueBind(queue,exchange,filter)
    consumer_tag = channel.basicConsume(incoming,queue)

def incoming(consumer_tag, routing_key, exchange, content):
    print("received: %s" % content)

#######################################################################################################################

if __name__ == "__main__":
    parser = parser()
    parser.add_option("-f","--filter",default="#",dest="filter",
                      help="filter for message routing keys")
    (options, args) = parser.parse_args()

    conn = connect(options)
    channel = conn.channel()

    subscribe(channel,options.exchange,options.filter)

    print("press ctrl-C to exit")
    while keep_running:
        time.sleep(1)
    print("shutting down")
    channel.close()
    conn.close()

#######################################################################################################################
